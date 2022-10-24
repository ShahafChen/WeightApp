import matplotlib.pyplot as plt


def build_graph(date_axe, weight_axe):
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.title('Your Weight By The Date')
    plt.plot(date_axe, weight_axe, 'ro')
    plt.show()
