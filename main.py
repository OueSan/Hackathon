import requests
from tkinter import ttk, messagebox, Tk

class PlantingAssistant:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Clima atual em {city}: {weather}, Temperatura: {temp}°C"
        else:
            return "Não foi possível obter as informações do tempo."

    def can_plant(self, temp, weather):
        if temp < 10 or temp > 30:
            return "A temperatura não está ideal para o plantio."
        elif 'chuva' in weather.lower():
            return "Não é ideal plantar com chuva."
        else:
            return "Boa condição para plantar."

    def check_ph(self, ph_level):
        if ph_level < 6.0:
            return (
                "O pH está baixo. Considere adicionar materiais naturais como calcário agrícola, "
                "cinzas de madeira ou conchas moídas para aumentar o pH. Teste o solo regularmente, para monitorar os níveis de pH e "
                "ajuste conforme necessário."
            )
        elif ph_level > 7.0:
            return (
                "O pH está alto. Considere adicionar matéria orgânica como composto de folhas, agulhas de pinheiro, "
                "turfa ou borra de café para diminuir o pH. Teste o solo regularmente, para monitorar os níveis de pH e "
                "ajuste conforme necessário."
            )
        else:
            return "O pH está adequado."

class PlantingApp(Tk):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.title("Planting Assistant")

        # Configurações da janela
        self.geometry("500x300")  # Define o tamanho inicial da janela
        self.minsize(500, 300)    # Define o tamanho mínimo da janela

        # Label e campo de entrada para a cidade
        ttk.Label(self, text="Insira seu local:").grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.city_entry = ttk.Entry(self)
        self.city_entry.grid(column=1, row=0, padx=10, pady=5, sticky="ew")

        # Label para mostrar o resultado do clima
        self.weather_result_label = ttk.Label(self, text="", wraplength=450)
        self.weather_result_label.grid(column=0, row=1, columnspan=3, padx=10, pady=5, sticky="w")

        # Label e campo de entrada para o pH
        ttk.Label(self, text="Insira o pH:").grid(column=0, row=2, padx=10, pady=5, sticky="w")
        self.ph_entry = ttk.Entry(self)
        self.ph_entry.grid(column=1, row=2, padx=10, pady=5, sticky="ew")

        # Labels para mostrar os resultados
        self.ph_result_label = ttk.Label(self, text="", wraplength=450)
        self.ph_result_label.grid(column=0, row=3, columnspan=3, padx=10, pady=5, sticky="w")

        self.planting_advice_label = ttk.Label(self, text="", wraplength=450)
        self.planting_advice_label.grid(column=0, row=4, columnspan=3, padx=10, pady=5, sticky="w")

        # Botões de ação
        self.get_weather_button = ttk.Button(self, text="Obter Clima", command=self.get_weather)
        self.get_weather_button.grid(column=0, row=5, padx=10, pady=5, sticky="ew")

        self.check_ph_button = ttk.Button(self, text="Verificar pH", command=self.check_ph)
        self.check_ph_button.grid(column=1, row=5, padx=10, pady=5, sticky="ew")

        # Configurar as colunas e linhas para se expandirem
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Entrada inválida", "Por favor, insira o nome da cidade.")
            return

        weather_info = self.assistant.get_weather(city)
        self.weather_result_label.config(text=weather_info)

        if "Clima atual em" in weather_info:
            try:
                weather_data = weather_info.split(", ")
                temp = float(weather_data[1].split(": ")[1].replace("°C", ""))
                weather = weather_data[0].split(": ")[1]
                planting_advice = self.assistant.can_plant(temp, weather)
                self.planting_advice_label.config(text=planting_advice)
            except (IndexError, ValueError):
                self.planting_advice_label.config(text="Não foi possível processar os dados climáticos.")
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
    api_key = "96b7d7524b7a7571fe675adc64ac39a0"  # Chave API 
    assistant = PlantingAssistant(api_key)
    app = PlantingApp(assistant)
    app.mainloop()
