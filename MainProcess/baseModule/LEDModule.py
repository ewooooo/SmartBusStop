from rgbmatrix import graphics,RGBMatrix, RGBMatrixOptions
import time

class baseLED():
    def __init__(self):
        
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.gpio_slowdown = 2
        self.matrix = RGBMatrix(options = options)


    def SET_LED_set(self,my_text):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("./5x7.bdf")
        font = graphics.Font()
        font.LoadFont("./10x20.bdf")
        textColor = graphics.Color(255, 255, 0)
        testlen = len(my_text)
        
        if testlen == 1:
            col=24
            col2=34
        elif testlen ==2:
            col=16
            col2=36
        elif testlen ==3:
            col=8
            col2=38
        elif testlen ==4:
            col=4
            col2=44
        elif testlen ==5:
            col=0
            col2=50
        elif testlen ==6:
            col=1
            col2=50
            font = graphics.Font()
            font.LoadFont("./8x13B.bdf")       

        
        graphics.DrawText(self.offscreen_canvas, font, col, 21, textColor, my_text)
        
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+6, 9, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 9, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 10, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 10, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+8, 10, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 11, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 11, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+8, 11, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 12, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 12, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 13, textColor, ".")
    
        graphics.DrawText(self.offscreen_canvas, font1, col2+2, 14, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+4, 14, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 14, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+1, 15, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 15, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 15, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+9, 15, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2, 16, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 16, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2, 17, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2, 18, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 18, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+7, 18, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+9, 18, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2, 19, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+1, 20, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+6, 20, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+9, 20, textColor, ".")
        
        graphics.DrawText(self.offscreen_canvas, font1, col2+2, 21, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+4, 21, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+5, 21, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+9, 21, textColor, ".")
        graphics.DrawText(self.offscreen_canvas, font1, col2+11, 21, textColor, ".")
        
        
    def OFF_LED_set(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.displaying = self.matrix.SwapOnVSync(self.offscreen_canvas)
    
    
    def SET_LED(self,my_text):
        self.SET_LED_set(my_text)
        self.displaying = self.matrix.SwapOnVSync(self.offscreen_canvas)
        
        
    def OFF_LED(self):
        self.OFF_LED_set()

if __name__ == "__main__":

    run_text = baseLED()
    while(True):
        run_text.SET_LED("70000")
        time.sleep(2)
        run_text.OFF_LED()
        time.sleep(2)
    

