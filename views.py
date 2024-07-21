import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm, SignUpForm, LoginForm
from .algorithm import Algoritmo
import io
import base64
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Persona, Cuenta, Rol

def plot_predictions(predictions_df):
    fig, ax = plt.subplots()
    width = 0.35  # Ancho de las barras

    estudiantes = predictions_df['Estudiante']
    probabilidad_aproximada = predictions_df['Probabilidad Aproximada de Deserción']
    prediccion_desercion = predictions_df['Predicción de Deserción']

    x = np.arange(len(estudiantes))  # Posiciones en el eje x

    ax.bar(x - width/2, probabilidad_aproximada, width, label='Probabilidad Aproximada de Deserción', color='lightblue')
    ax.bar(x + width/2, prediccion_desercion, width, label='Predicción de Deserción', color='blue', alpha=0.7)

    ax.set_xlabel('Estudiantes')
    ax.set_ylabel('Probabilidad de Deserción')
    ax.set_title('Probabilidad de Deserción Final por Estudiante')
    ax.set_xticks(x)
    ax.set_xticklabels(estudiantes, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def inicio(request):
    predictions = {}
    graphics = {}
    data_per_cycle = {}
    file_uploaded = False
    general_stats = {}

    if request.method == 'POST' and 'predict' in request.POST:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['archivo']
            data = pd.read_csv(csv_file)

            required_columns = {'nombre', 'promedio_academico', 'asistencia_clases', 'materias_reprobadas', 'apoyo_familiar', 'situacion_socioeconomica', 'trabaja', 'distancia_universidad'}
            
            if not required_columns.issubset(data.columns):
                messages.error(request, 'El archivo CSV no contiene las columnas requeridas.')
                return render(request, 'inicio/inicio.html', {
                    'form': form,
                    'predictions': predictions,
                    'graphics': graphics,
                    'data_per_cycle': json.dumps(data_per_cycle),
                    'file_uploaded': file_uploaded,
                    'general_stats': general_stats
                })

            ciclos = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            all_predictions = []

            for ciclo in ciclos:
                ciclo_data = data
                algoritmo = Algoritmo(ciclo_data)
                ciclo_predictions = algoritmo.euler_method(1, 1, 1, 2, ciclo)
                predictions[ciclo] = ciclo_predictions.to_html(index=False)

                estudiantes = ciclo_predictions['Estudiante']
                probabilidades = ciclo_predictions['Probabilidad Aproximada de Desercion']
                predicciones_futuras = ciclo_predictions['Predicción de Desercion']
                data_per_cycle[str(ciclo)] = {
                    'estudiantes': estudiantes.tolist(),
                    'probabilidades': probabilidades.tolist(),
                    'predicciones_futuras': predicciones_futuras.tolist()
                }
                all_predictions.append(ciclo_predictions)

            if all_predictions:
                all_predictions_df = pd.concat(all_predictions)
                general_stats['total_estudiantes'] = all_predictions_df.shape[0]
                general_stats['estudiantes_alta_desercion'] = all_predictions_df[all_predictions_df['Riesgo'] == 'Alta'].shape[0]
                general_stats['estudiantes_media_desercion'] = all_predictions_df[all_predictions_df['Riesgo'] == 'Media'].shape[0]
                general_stats['estudiantes_baja_desercion'] = all_predictions_df[all_predictions_df['Riesgo'] == 'Baja'].shape[0]
                general_stats['ciclo_con_mayor_desercion'] = max(ciclos, key=lambda c: all_predictions_df[all_predictions_df['Estudiante'].str.contains(f'_{c}$')]['Probabilidad Aproximada de Desercion'].mean())
                general_stats['ciclo_con_menor_desercion'] = min(ciclos, key=lambda c: all_predictions_df[all_predictions_df['Estudiante'].str.contains(f'_{c}$')]['Probabilidad Aproximada de Desercion'].mean())
                general_stats['porcentaje_promedio_desercion'] = all_predictions_df['Probabilidad Aproximada de Desercion'].mean() * 20

            file_uploaded = True
    else:
        form = CSVUploadForm()

    return render(request, 'inicio/inicio.html', {
        'form': form,
        'predictions': predictions,
        'graphics': graphics,
        'data_per_cycle': json.dumps(data_per_cycle),
        'file_uploaded': file_uploaded,
        'general_stats': general_stats
    })

def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST['correo']
        # Aquí va la lógica para enviar el enlace de recuperación de contraseña.
        return render(request, '/registration/recuperar_contrasena.html', {'mensaje': 'Enlace enviado a su correo electrónico'})
    return render(request, 'registration/recuperar_contrasena.html')

def ayuda(request):
    return render(request, 'inicio/ayuda.html')

def signup(request):
    roles = Rol.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.set_password(form.cleaned_data['password1'])
            cuenta.save()
            login(request, cuenta)
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('inicio')
        else:
            messages.error(request, 'Formulario no válido')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'roles': roles})

@login_required
def gestionar_usuarios(request):
    if request.method == 'POST':
        cuenta_id = request.POST.get('cuenta_id')
        cuenta = Cuenta.objects.get(id=cuenta_id)
        cuenta.is_active = not cuenta.is_active
        cuenta.save()
        return redirect('gestionar_usuarios')
    
    cuentas = Cuenta.objects.all()
    return render(request, 'registration/gestionar_usuarios.html', {'cuentas': cuentas})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Email: {email}, Password: {password}")  # Mensaje de depuración
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("Autenticación exitosa")  # Mensaje de depuración
                return redirect('inicio')  # Redirige a la página de inicio o donde desees
            else:
                print("Error de autenticación")  # Mensaje de depuración
                messages.error(request, 'Correo o contraseña incorrectos')
        else:
            print("Formulario no válido")  # Mensaje de depuración
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})