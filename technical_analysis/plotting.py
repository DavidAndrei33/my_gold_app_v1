import matplotlib.pyplot as plt

def generate_price_chart(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Price'])
    plt.title('Evoluția prețului')
    plt.xlabel('Data')
    plt.ylabel('Preț')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
