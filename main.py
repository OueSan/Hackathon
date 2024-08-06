import requests
import tkinter as tk
from tkinter import ttk, messagebox

class PlantingAssistant:
    def __init__(self, api_key):
        self.ph_low_threshold = 5.5
        self.ph_high_threshold = 7.5
        self.api_key = api_key

    def check_ph(self, ph_level):
        if ph_level < self.ph_low_threshold:
            return self.low_ph_advice()
        elif ph_level > self.ph_high_threshold:
            return self.high_ph_advice()
        else:
            return "O pH do solo está dentro do intervalo ideal para a maioria das plantas."

    def low_ph_advice(self):
        return (
            "O pH do solo está baixo. Considere adicionar materiais naturais como calcário agrícola, "
            "cinzas de madeira ou conchas moídas para aumentar o pH. Certifique-se de testar o solo regularmente "
            "e adicionar pequenas quantidades por vez, seguindo as recomendações naturais."
        )

    def high_ph_advice(self):
        return (
            "O pH do solo está alto. Considere adicionar matéria orgânica como composto de folhas, "
            "agulhas de pinheiro, turfa ou borra de café para diminuir o pH. Teste o solo regularmente "
            "para monitorar os níveis de pH e ajuste conforme necessário."
        )

    def get_weather(self, city):
        url = f"api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={api_key}"
        response = requests.get(url)
        data = response.json()

        # Adicione esta linha para verificar a resposta da API
        print(data)

        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            return f"Clima atual em {city}: {weather}, Temperatura: {temp}°C, Umidade: {humidity}%"
        else:
            return f"Não foi possível obter os dados climáticos. Verifique o nome da cidade e tente novamente. Erro: {data.get('message', 'Desconhecido')}"

    def can_plant(self, temp, weather):
        if temp < 10 or temp > 30:
            return "A temperatura não está ideal para o plantio."
        if "rain" in weather.lower():
            return "Está chovendo, evite plantar agora."
        return "As condições climáticas estão boas para o plantio."

class PlantingApp(tk.Tk):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.title("Assistente de Plantio")

        self.city_label = ttk.Label(self, text="Cidade:")
        self.city_label.grid(column=0, row=0, padx=10, pady=5)
        self.city_entry = ttk.Entry(self)
        self.city_entry.grid(column=1, row=0, padx=10, pady=5)
        self.weather_button = ttk.Button(self, text="Obter Clima", command=self.get_weather)
        self.weather_button.grid(column=2, row=0, padx=10, pady=5)

        self.weather_result_label = ttk.Label(self, text="")
        self.weather_result_label.grid(column=0, row=1, columnspan=3, padx=10, pady=5)

        self.ph_label = ttk.Label(self, text="Nível de pH do Solo:")
        self.ph_label.grid(column=0, row=2, padx=10, pady=5)
        self.ph_entry = ttk.Entry(self)
        self.ph_entry.grid(column=1, row=2, padx=10, pady=5)
        self.ph_button = ttk.Button(self, text="Verificar pH", command=self.check_ph)
        self.ph_button.grid(column=2, row=2, padx=10, pady=5)

        self.ph_result_label = ttk.Label(self, text="")
        self.ph_result_label.grid(column=0, row=3, columnspan=3, padx=10, pady=5)

        self.planting_advice_label = ttk.Label(self, text="")
        self.planting_advice_label.grid(column=0, row=4, columnspan=3, padx=10, pady=5)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Entrada inválida", "Por favor, insira o nome da cidade.")
            return

        weather_info = self.assistant.get_weather(city)
        self.weather_result_label.config(text=weather_info)

        if "Clima atual em" in weather_info:
            weather_data = weather_info.split(", ")
            temp = float(weather_data[1].split(": ")[1].replace("°C", ""))
            weather = weather_data[0].split(": ")[1]
            planting_advice = self.assistant.can_plant(temp, weather)
            self.planting_advice_label.config(text=planting_advice)
        else:
            self.planting_advice_label.config(text="")

    def check_ph(self):
        try:
            ph_level = float(self.ph_entry.get())
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Por favor, insira um valor numérico válido para o pH.")
            return

        advice = self.assistant.check_ph(ph_level)
        self.ph_result_label.config(text=advice)

if __name__ == "__main__":
    api_key = "96b7d7524b7a7571fe675adc64ac39a0"  # Substitua pela sua chave de API
    assistant = PlantingAssistant(api_key)
    app = PlantingApp(assistant)
    app.mainloop()
