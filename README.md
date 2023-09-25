# ECB Data Scraper and Database Updater

Este proyecto está diseñado para obtener datos económicos de la European Central Bank (ECB), visualizarlos en un gráfico y almacenarlos en una base de datos MySQL. Además, consulta el calendario de reuniones de la ECB para identificar la próxima reunión relacionada con tasas de interés.

## Funcionalidades

- **Obtención de Datos**: El programa obtiene datos económicos de la ECB (concretamente la tasa de interes) a través de una solicitud web , los almacena en un DataFrame de Pandas.

- **Visualización de Datos**: Los datos obtenidos se visualizan en un gráfico que muestra las observaciones en función del tiempo.

- **Almacenamiento en Base de Datos**: Los datos también se almacenan en una base de datos MySQL local. Si ya existen datos para una fecha determinada, se actualizan en lugar de crear una nueva entrada.

- **Calendario de Reuniones de la ECB**: El programa realiza web scraping en la página de calendario de reuniones de la ECB y muestra la fecha de la próxima reunión donde se discutirán tasas de interés.

## Requisitos

- Python 3.x
- Bibliotecas Python: pandas, requests, matplotlib, mysql-connector-python, beautifulsoup4
- MySQL

