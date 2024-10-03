from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from MotorInferencia import MotorDeInferencia


app = Flask(__name__)



class CalculadorPresupuesto:
    @staticmethod
    def obtener_precio_material(material):
        # Diccionario con las URLs de las páginas web para obtener los precios de los materiales
        urls = {
            'cemento': "https://materialescortes.com.mx/cemento-cruz-azul-50-kg",
            'arena': "https://materialescortes.com.mx/arena-ligera",
            'grava': "https://materialescortes.com.mx/grava-ligera",
             'block': 'https://materialescortes.com.mx/pieza-de-block-ligero-o-pesado-macizo',
        }

        # Hacer scraping para obtener el precio del material
        if material in urls:
            response = requests.get(urls[material])
            soup = BeautifulSoup(response.content, 'html.parser')
            precio_element = soup.find("h2", {"class": "product-heading__pricing"})
            if precio_element:
                precio_texto = precio_element.text
                precio_texto = precio_texto.replace("$", "").replace("MXN", "").strip()
                precio = float(precio_texto)
            else:
                precio = 0
        else:
            # Manejar el caso de otros materiales si es necesario
            precio = 0

        return precio

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_presupuesto', methods=['POST'])
def calcular_presupuesto():
    data = request.get_json()
    materiales = ['cemento','arena', 'grava', 'block', 'castillos']
    precios = {material: CalculadorPresupuesto.obtener_precio_material(material) for material in materiales}
    total = sum(precios[material] * data.get(material, 0) for material in materiales)
    return jsonify(total)


###############################
###############################

@app.route('/calcular_precio_metro_cuadrado', methods=['POST'])
def calcular_precio_metro_cuadrado():
    data = request.get_json()
    
    # Obtener precios por metro cuadrado
    precios = {
        'habitacion': float(data.get('precio_habitacion', 0)),
        'bano': float(data.get('precio_bano', 0)),
        'cocina': float(data.get('precio_cocina', 0)),
        'sala': float(data.get('precio_sala', 0)),
        'servicio': float(data.get('precio_servicio', 0)),
        'pasillo': float(data.get('precio_pasillo', 0)),
        'cochera': float(data.get('precio_cochera', 0)),
        'patio': float(data.get('precio_patio', 0))
    }
    
    # Inicializar variables de áreas, precios y bloques
    area_total = 0
    precio_total = 0
    bloques_total = 0
    espesor_concreto=0.1
    
    # Calcular el precio y la cantidad de bloques para las habitaciones si se proporciona información
    num_habitaciones = int(data.get('num_habitaciones', 0))
    precio_habitaciones = 0
    bloques_habitaciones = 0
    if num_habitaciones > 0:
        tamano_habitacion = data.get('tamano_habitacion', '0x0')
        largo_habitacion, ancho_habitacion = map(float, tamano_habitacion.split('x'))
        area_habitacion = largo_habitacion * ancho_habitacion 
        altura_hab=(largo_habitacion* 2.4) + ancho_habitacion*2.4
        altura_hab = altura_hab *2
        precio_habitaciones = area_habitacion * num_habitaciones * precios['habitacion']
        bloques_habitaciones = altura_hab * 12.5 * 1.05 * num_habitaciones
        area_total += area_habitacion * num_habitaciones
        precio_total += precio_habitaciones
        bloques_total += bloques_habitaciones
    
    # Calcular el precio y la cantidad de bloques para los baños si se proporciona información
    num_banos = int(data.get('num_banos', 0))
    precio_banos = 0
    bloques_banos = 0
    if num_banos > 0:
        tamano_bano = data.get('tamano_bano', '0x0')
        largo_bano, ancho_bano = map(float, tamano_bano.split('x'))
        area_bano = largo_bano * ancho_bano
        altura_ban=(largo_habitacion* 2.4) + ancho_habitacion*2.4
        altura_ban = altura_ban *2
        precio_banos = area_bano * num_banos * precios['bano']
        bloques_banos = altura_ban * 12.5 * 1.05 * num_banos
        area_total += area_bano * num_banos
        precio_total += precio_banos
        bloques_total += bloques_banos
      
    
    # Calcular el precio y la cantidad de bloques para la cocina si se proporciona información
    precio_cocina = 0
    bloques_cocina = 0
    if 'tamano_cocina' in data:
        tamano_cocina = data.get('tamano_cocina', '0x0')
        largo_cocina, ancho_cocina = map(float, tamano_cocina.split('x'))
        area_cocina = largo_cocina * ancho_cocina
        altura_coc=(largo_habitacion* 2.4) + ancho_habitacion*2.4
        altura_coc = altura_coc *2
        precio_cocina = area_cocina * precios['cocina']
        bloques_cocina = altura_coc * 12.5 * 1.05
        area_total += area_cocina
        precio_total += precio_cocina
        bloques_total += bloques_cocina

    # Calcular el precio y la cantidad de bloques para la sala si se proporciona información
    precio_sala = 0
    bloques_sala = 0
    if 'tamano_sala' in data:
        tamano_sala = data.get('tamano_sala', '0x0')
        largo_sala, ancho_sala = map(float, tamano_sala.split('x'))
        area_sala = largo_sala * ancho_sala
        altura_sal=(largo_habitacion* 2.4) + ancho_habitacion*2.4
        altura_sal = altura_sal *2
        precio_sala = area_sala * precios['sala']
        bloques_sala = altura_sal * 12.5 * 1.05
        area_total += area_sala
        precio_total += precio_sala
        bloques_total += bloques_sala
    
    # Calcular el precio del área de servicio si se proporciona información
    precio_servicio = 0
    if 'tamano_servicio' in data:
        tamano_servicio = data.get('tamano_servicio', '0x0')
        largo_servicio, ancho_servicio = map(float, tamano_servicio.split('x'))
        area_servicio = largo_servicio * ancho_servicio
        precio_servicio = area_servicio * precios['servicio']
        area_total += area_servicio
        precio_total += precio_servicio
    
    # Calcular el precio de la cochera si se proporciona información
    precio_cochera = 0
    if 'tamano_cochera' in data:
        tamano_cochera = data.get('tamano_cochera', '0x0')
        largo_cochera, ancho_cochera = map(float, tamano_cochera.split('x'))
        area_cochera = largo_cochera * ancho_cochera
        precio_cochera = area_cochera * precios['cochera']
        area_total += area_cochera
        precio_total += precio_cochera
    
    # Calcular el precio del patio si se proporciona información
    precio_patio = 0
    if 'tamano_patio' in data:
        tamano_patio = data.get('tamano_patio', '0x0')
        largo_patio, ancho_patio = map(float, tamano_patio.split('x'))
        area_patio = largo_patio * ancho_patio
        precio_patio = area_patio * precios['patio']
        area_total += area_patio
        precio_total += precio_patio
    


        volumen_concreto = area_total * espesor_concreto

    # Calculate concrete volume and material quantities
        volumen_concreto = area_total * espesor_concreto
        cantidad_cemento = 160 * volumen_concreto
        cantidad_arena = 0.55 * volumen_concreto
        cantidad_grava = 1.03 * volumen_concreto

        cantidad_cemento=cantidad_cemento


    return jsonify({

        'cantidad_cemento': cantidad_cemento,
        'cantidad_arena': cantidad_arena,
        'cantidad_grava': cantidad_grava,
        #
        'precio_total': precio_total,
        'precio_habitaciones': precio_habitaciones,
        'precio_banos': precio_banos,
        'precio_cocina': precio_cocina,
        'precio_sala': precio_sala,
        'precio_servicio': precio_servicio,
        'precio_cochera': precio_cochera,
        'precio_patio': precio_patio,
        
         # Agregar precios para otras áreas si es necesario
    'bloques_total': bloques_total,
    'bloques_habitaciones': bloques_habitaciones,
    'bloques_banos': bloques_banos,
    'bloques_cocina': bloques_cocina,
    'bloques_sala': bloques_sala,
    # Agregar bloques para otras áreas si es necesario
    'area_total': area_total
    })
 



#################################################
###############################################


@app.route('/calcular_combinaciones', methods=['POST'])
def calcular_combinaciones():
    # Obtener los datos del formulario
    tamano_terreno = request.form['tamano_terreno']
    tamano_sala = request.form['tamano_sala']
    tamano_servicio = request.form['tamano_servicio']
    tamano_cocina = request.form['tamano_cocina']
    tamano_patio = request.form['tamano_patio']
    tamano_cochera = request.form['tamano_cochera']
    tamano_sala_personalizado = request.form['tamano_sala_personalizado']
    tamano_servicio_personalizado = request.form['tamano_servicio_personalizado']
    tamano_cocina_personalizado = request.form['tamano_cocina_personalizado']
    tamano_patio_personalizado = request.form['tamano_patio_personalizado']
    tamano_cochera_personalizado = request.form['tamano_cochera_personalizado']
    
    planta = request.form['planta']  # Agregar línea para obtener el tipo de planta

    # Calcular las combinaciones
    motor = MotorDeInferencia()
    if planta == "planta_alta":
        area_restante_alta, combinaciones, area_restante_baja,tamanos_areas_altas = motor.calcular_combinaciones(
            tamano_terreno, tamano_sala, tamano_servicio, tamano_cocina, tamano_patio, tamano_cochera,
            tamano_sala_personalizado, tamano_servicio_personalizado, tamano_cocina_personalizado,
            tamano_patio_personalizado, tamano_cochera_personalizado, planta="planta_alta"
        )

        combinaciones_json = []
        for combinacion in combinaciones:
            combinaciones_json.append({
                'habitaciones': combinacion[0],
                'tamano_habitacion': combinacion[2] + " m²",
                'banos': combinacion[1],
                'tamano_bano': combinacion[3] + " m²",
                'metros_sin_asignar': combinacion[4]
            })

        # Devolver las combinaciones y los tamaños de todas las áreas como respuesta en formato JSON
        return jsonify({'area_restante_alta': area_restante_alta,'tamanos_areas_altas':tamanos_areas_altas, 'area_restante_baja': area_restante_baja, 'combinaciones': combinaciones_json})
    else:
        area_restante, combinaciones, tamanos_areas = motor.calcular_combinaciones(
            tamano_terreno, tamano_sala, tamano_servicio, tamano_cocina, tamano_patio, tamano_cochera,
            tamano_sala_personalizado, tamano_servicio_personalizado, tamano_cocina_personalizado,
            tamano_patio_personalizado, tamano_cochera_personalizado
        )

        combinaciones_json = []
        for combinacion in combinaciones:
            combinaciones_json.append({
                'habitaciones': combinacion[0],
                'tamano_habitacion': combinacion[2] + " m²",
                'banos': combinacion[1],
                'tamano_bano': combinacion[3] + " m²",
                'metros_sin_asignar': combinacion[4]
            })

        # Devolver las combinaciones y los tamaños de todas las áreas como respuesta en formato JSON
        return jsonify({'area_restante': area_restante, 'tamanos_areas': tamanos_areas, 'combinaciones': combinaciones_json})

if __name__ == "__main__":
    app.run(debug=True)
