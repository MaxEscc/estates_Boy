class MotorDeInferencia:
    def __init__(self):
        pass

    def calcular_area(self, tamano, tipo):
        # Definir tamaños predefinidos y personalizados
        tamanos_predefinidos = {
            'sala_comedor': {'pequeña': 9, 'mediana': 12, 'grande': 18},
            'servicio': {'pequeño': 6, 'mediano': 9, 'grande': 12},
            'cocina': {'pequeña': 5.2, 'mediana': 9, 'grande': 14},
            'habitacion': {'pequeña': 9, 'mediana': 12, 'grande': 15},
            'baño': {'pequeño': 3.6, 'mediano': 5, 'grande': 7},
            'patio': {'pequeño': 6, 'mediano': 12, 'grande': 16},
            'cochera': {'pequeña': 10, 'mediana': 15, 'grande': 20}
        }

        if tipo in tamanos_predefinidos and tamano in tamanos_predefinidos[tipo]:
            return tamanos_predefinidos[tipo][tamano]
        elif tipo == 'personalizado' and tamano:
            try:
                x, y = map(float, tamano.split('x'))
                return x * y
            except ValueError:
                return 0
        else:
            return 0

    def calcular_combinaciones(self, tamano_terreno, tamano_sala, tamano_servicio, tamano_cocina, tamano_patio, tamano_cochera,
                                tamano_sala_personalizado, tamano_servicio_personalizado, tamano_cocina_personalizado,
                                tamano_patio_personalizado, tamano_cochera_personalizado, planta="planta_baja"):
        if planta == "planta_baja":
            # Procesar como planta baja
            # Extraer los valores numéricos del tamaño del terreno
            largo_terreno, ancho_terreno = map(float, tamano_terreno.split('x'))

            # Calcular el área total del terreno
            area_terreno = largo_terreno * ancho_terreno

            # Calcular el área ocupada por cada tipo de espacio
            area_sala = self.calcular_area(tamano_sala, "sala_comedor")
            area_servicio = self.calcular_area(tamano_servicio, "servicio")
            area_cocina = self.calcular_area(tamano_cocina, "cocina")
            area_patio = self.calcular_area(tamano_patio, "patio")
            area_cochera = self.calcular_area(tamano_cochera, "cochera")

            # Sumar el área personalizada al área total de cada tipo de espacio
            area_sala_personalizado = self.calcular_area(tamano_sala_personalizado, "personalizado")
            area_servicio_personalizado = self.calcular_area(tamano_servicio_personalizado, "personalizado")
            area_cocina_personalizado = self.calcular_area(tamano_cocina_personalizado, "personalizado")
            area_patio_personalizado = self.calcular_area(tamano_patio_personalizado, "personalizado")
            area_cochera_personalizado = self.calcular_area(tamano_cochera_personalizado, "personalizado")

            area_sala += area_sala_personalizado
            area_servicio += area_servicio_personalizado
            area_cocina += area_cocina_personalizado
            area_patio += area_patio_personalizado
            area_cochera += area_cochera_personalizado

            # Imprimir el tamaño de todas las áreas
            print("Tamaño de todas las áreas:")
            print(f"Sala: {area_sala} m²")
            print(f"Servicio: {area_servicio} m²")
            print(f"Cocina: {area_cocina} m²")
            print(f"Patio: {area_patio} m²")
            print(f"Cochera: {area_cochera} m²")

            # Calcular el área restante
            area_restante = area_terreno - area_sala - area_servicio - area_cocina - area_patio - area_cochera

            # Redondear el área restante para una mejor presentación
            area_restante = round(area_restante, 2)

            # Mostrar los metros cuadrados restantes
            print(f"Metros cuadrados restantes: {area_restante}")

            # Generar todas las combinaciones posibles de habitaciones y baños
            combinaciones = []
            for num_habitaciones in range(1, int(area_restante // 9) + 1):  # Comienza desde 1 habitación
                for num_banos in range(1, int(area_restante // 7) + 1):  # Comienza desde 1 baño
                    for tamano_habitacion in ['pequeña', 'mediana', 'grande']:
                        for tamano_bano in ['pequeño', 'mediano', 'grande']:
                            area_ocupada = (num_habitaciones * self.calcular_area(tamano_habitacion, "habitacion")) + (
                                        num_banos * self.calcular_area(tamano_bano, "baño"))
                            if area_ocupada <= area_restante and num_habitaciones != 0 and num_banos != 0:
                                combinaciones.append(
                                    (num_habitaciones, num_banos, tamano_habitacion, tamano_bano,
                                     area_restante - area_ocupada))

            # Redondear los metros sin asignar en las combinaciones
            combinaciones = [(num_habitaciones, num_banos, tamano_habitacion, tamano_bano, round(metros_sin_asignar, 2))
                             for num_habitaciones, num_banos, tamano_habitacion, tamano_bano, metros_sin_asignar in combinaciones]

            # Mostrar las combinaciones posibles
            print("Combinaciones posibles de habitaciones y baños:")
            for combinacion in combinaciones:
                print(
                    f"Habitaciones: {combinacion[0]} ({combinacion[2]}), Baños: {combinacion[1]} ({combinacion[3]}), Metros sin asignar: {combinacion[4]}")

             # Almacenar los tamaños de las áreas en variables
            tamanos_areas = {
                'Sala': area_sala,
                'Servicio': area_servicio,
                'Cocina': area_cocina,
                'Patio': area_patio,
                'Cochera': area_cochera
            }

            # Devolver el área restante y las combinaciones junto con los tamaños de las áreas
            return area_restante, combinaciones, tamanos_areas

       
        elif planta == "planta_alta":
                # Calcular el área ocupada por la sala y la cocina en planta baja
                area_sala_baja = self.calcular_area(tamano_sala, "sala_comedor")
                area_cocina_baja = self.calcular_area(tamano_cocina, "cocina")

                # Calcular el área restante en la planta baja
                largo_terreno, ancho_terreno = map(float, tamano_terreno.split('x'))
                area_terreno = largo_terreno * ancho_terreno
                area_sala_baja = self.calcular_area(tamano_sala, "sala_comedor")
                area_servicio_baja = self.calcular_area(tamano_servicio, "servicio")
                area_cocina_baja = self.calcular_area(tamano_cocina, "cocina")
                area_patio_baja = self.calcular_area(tamano_patio, "patio")
                area_cochera_baja = self.calcular_area(tamano_cochera, "cochera")

                # Sumar el área personalizada al área total de cada tipo de espacio en planta baja
                area_sala_baja += self.calcular_area(tamano_sala_personalizado, "personalizado")
                area_servicio_baja += self.calcular_area(tamano_servicio_personalizado, "personalizado")
                area_cocina_baja += self.calcular_area(tamano_cocina_personalizado, "personalizado")
                area_patio_baja += self.calcular_area(tamano_patio_personalizado, "personalizado")
                area_cochera_baja += self.calcular_area(tamano_cochera_personalizado, "personalizado")

                area_restante_baja = area_terreno - area_sala_baja - area_servicio_baja - area_cocina_baja - area_patio_baja - area_cochera_baja

                # Usar el área de la sala y la cocina de la planta baja para generar combinaciones en planta alta
                area_restante_alta = area_sala_baja + area_cocina_baja

                # Generar combinaciones de habitaciones y baños en planta alta basadas en el área de la sala y la cocina de la planta baja
                combinaciones = []
                for num_habitaciones in range(1, int(area_restante_alta // 9) + 1):  # Comienza desde 1 habitación
                    for num_banos in range(1, int(area_restante_alta // 7) + 1):  # Comienza desde 1 baño
                        for tamano_habitacion in ['pequeña', 'mediana', 'grande']:
                            for tamano_bano in ['pequeño', 'mediano', 'grande']:
                                area_ocupada = (num_habitaciones * self.calcular_area(tamano_habitacion, "habitacion")) + (
                                            num_banos * self.calcular_area(tamano_bano, "baño"))
                                if area_ocupada <= area_restante_alta and num_habitaciones != 0 and num_banos != 0:
                                    combinaciones.append(
                                        (num_habitaciones, num_banos, tamano_habitacion, tamano_bano,
                                        area_restante_alta - area_ocupada))

                # Redondear los metros sin asignar en las combinaciones en planta alta
                combinaciones = [(num_habitaciones, num_banos, tamano_habitacion, tamano_bano, round(metros_sin_asignar, 2))
                                for num_habitaciones, num_banos, tamano_habitacion, tamano_bano, metros_sin_asignar in combinaciones]

                # Imprimir las combinaciones posibles en planta alta
                print("Combinaciones posibles de habitaciones y baños en planta alta:")
                for combinacion in combinaciones:
                    print(
                        f"Habitaciones: {combinacion[0]} ({combinacion[2]}), Baños: {combinacion[1]} ({combinacion[3]}), Metros sin asignar: {combinacion[4]}")


                tamanos_areas_altas = {
                    'Sala': area_sala_baja,
                    'Servicio': area_servicio_baja,
                    'Cocina': area_cocina_baja,
                    'Patio': area_patio_baja,
                    'Cochera': area_cochera_baja
                }
                        # Devolver el área restante alta y las combinaciones
                return area_restante_alta, combinaciones, area_restante_baja,tamanos_areas_altas
