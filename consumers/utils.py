import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(average_rating):
    plt.figure(figsize=(6, 4))
    plt.bar(['Average Rating'], [average_rating], color='blue')
    plt.ylim(0, 5)  
    plt.title('Facebeat Rating')
    plt.ylabel('Rating')

    # Generate the graph and return it as a base64 string
    graph = get_graph()
    plt.clf()  
    return graph
