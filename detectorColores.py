from tkinter import Tk,Label,ttk,OptionMenu,StringVar,Frame,END
from tkinter.constants import END
from PIL import Image, ImageTk
import cv2
import numpy as np
import imutils

class Detector: 
    def __init__(self):
        self.capturar = None
        root = Tk()
        root.title('Proyecto Automatas')
        root.resizable(0,0)
        root.iconbitmap('icono.ico')

        btnIniciar = ttk.Button(root, text="Iniciar", width=45, command=self.iniciar)
        btnIniciar.grid(column=0, row=2, padx=5, pady=5)
        btnFinalizar = ttk.Button(root, text="Finalizar", width=45, command=self.finalizar)
        btnFinalizar.grid(column=1, row=2, padx=5, pady=5)

        self.labelInformacion= Label(root, text='Todas las compuertas estan cerradas')
        self.labelInformacion.grid(column=0,row=1,columnspan=2)

        values = StringVar(root)
        values.set('Seleccionar')
        options = ('Rojo','Amarillo','Azul')

        info = Frame(root)
        info.grid(row=3,column=0, columnspan=2)

        self.opcionesMenu = OptionMenu(info,values,*options)
        self.opcionesMenu.grid(column=0,row=3)

        self.peso = ttk.Entry(info)
        self.peso.grid(column=1, row=3 , padx=1)

        self.cantidad = self.cantidad = ttk.Entry(info)
        self.cantidad.grid(column=2, row=3 , padx=1)
        self.cantidad.config(state='readonly')

        self.calcular = ttk.Button(info, text='Cantidad', command = lambda:[self.calcularCantidad(values.get())])
        self.calcular.grid(column=3,row=3)


        self.lblVideo = Label(root)
        self.lblVideo.grid(column=0, row=0, columnspan=2)

        root.mainloop()

    def abrirCompuerta(self,color):

        if color == (255,0,0):
            self.labelInformacion.config(text='Roja : Cerrada | Azul : Abierta | Amarilla : Cerrada')
        elif color == (0,255,255):
            self.labelInformacion.config(text='Roja : Cerrada | Azul : Cerrada | Amarilla : Abierta')
        elif color == (0,0,255):
            self.labelInformacion.config(text='Roja : Abierta | Azul : Cerrada | Amarilla : Cerrada')

    def dibujarObjeto(self,mascara,color):
        # if color == (0,0,0) : 
        #     self.abrirCompuerta(color) 
        #     return
        contornos,_ = cv2.findContours(mascara,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > 8000 and area< 40000:
                nContorno = cv2.convexHull(contorno)
                cv2.drawContours(self.frame,[nContorno], 0, color ,2)

                self.abrirCompuerta(color)

    def iniciar(self):
        self.capturar = cv2.VideoCapture(0)
        self.ver()

    def ver(self):

        
        amarilloMin = np.array([15,100,20],np.uint8)
        amarilloMax = np.array([45,255,255],np.uint8)

        azulMin = np.array([100,100,20],np.uint8)
        azulMax = np.array([125,255,255],np.uint8)

        rojoMin = np.array([0,100,20],np.uint8)
        rojoMax = np.array([8,255,255],np.uint8)

        rojoMin2 = np.array([175,100,20],np.uint8)
        rojoMax2 = np.array([179,255,255],np.uint8)


        if self.capturar is not None:
            
            rec,self.frame = self.capturar.read()

            if rec == True:

                frameHSV = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

                colorRojo = cv2.inRange(frameHSV,rojoMin,rojoMax)

                colorRojo2 = cv2.inRange(frameHSV,rojoMin2,rojoMax2)
                    
                colorRojo = cv2.add(colorRojo,colorRojo2)
                    
                colorAzul = cv2.inRange(frameHSV, azulMin, azulMax)
                    
                colorAmarillo = cv2.inRange(frameHSV, amarilloMin, amarilloMax)

                # colorNegro = cv2.inRange(frameHSV,negroMin,negroMax)

                    
                self.dibujarObjeto(colorRojo,(0,0,255))
                self.dibujarObjeto(colorAzul,(255,0,0))
                self.dibujarObjeto(colorAmarillo,(0,255,255))
                # # self.dibujarObjeto(colorNegro, (0,0,0)            
                self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
                self.frame = imutils.resize(self.frame, width=640)
                img = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.lblVideo.config(image=img)
                self.lblVideo.image = img
                self.lblVideo.after(10, self.ver)
            else:
                self.lblVideo.image = ""
                self.capturar.release()

    def finalizar(self):
        self.capturar.release()
        self.lblVideo.configure(image='')
        self.labelInformacion.config(text='Todas las compuertas estan cerradas')

    def calcularCantidad(self,color):
        print(color)
        if color == 'Amarillo':
            peso = 100
        elif color == 'Rojo':
            peso = 50
        elif color == 'Azul':
            peso = 80
        
        
        self.cantidad.config(state='enabled')
        self.cantidad.delete(0,END)
        self.cantidad.insert(0,int(int(self.peso.get())/peso))
        self.cantidad.config(state='disabled')


if __name__ == '__main__':
    app = Detector()