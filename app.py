
from fastapi import FastAPI
from pydantic import BaseModel
import time
from decouple import config

#SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = FastAPI()

users = []

horaActual = time.strftime('%H:%M:%S')
procesadoPorPy = 'procesado por Python '+ horaActual + 'hs' + ' en /msPython'

#Modelo
class User(BaseModel):
    idCliente: int
    nombre: str
    dni:  str
    telefono: str
    email:  str 
    procesadoPor:  str 

@app.get("/")
def read_root():
    return users


@app.post("/msPython")
def get_post(user: User):
    #Guardo el objeto que indica que el microservicio en Python fue utilizado
    users.append(user.dict())

    if(len(users) > 1):
       user.idCliente = user.idCliente + 1
       user.procesadoPor = procesadoPorPy
       users.append(user.dict())
       #print(users[2]);
       enviarCorreo()
    
    
    #Guardo el json que me envia Node en el array users[]
    return user;


def enviarCorreo():

    message = Mail(
    from_email='diegoalbarracin0@gmail.com',
    to_emails='diegosteamnew@hotmail.com',
    subject='TP Microservicios Node, Go y Python',
    html_content='<strong style="color:green">' + str(users[0]) +'<strong>' + ',<br><br>' + '<strong style="color:blue">' + str(users[0]) +'<strong>' + ',<br><br>' + '<strong style="color:yellow">' + str(users[0]) +'<strong>' + ',<br><br>')

    try:
        sg =SendGridAPIClient(config('TOKEN'))
        response = sg.send(message)
    except Exception as e:
        print("Error en envio de mail")