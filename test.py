if __name__ == "__main__":
    import time
    import sys
    import console
    from widget import *
    #from layouts import *
    from textwidgets import *
    from shapes import *
    from decorators import *
    from lines import *
    #from controls import *
    from events import *
    #from keyinput import *
    from colour import *
    
    #string = "".join([chr(c) for c in (CHAR_HLINE,CHAR_NE,CHAR_TEEE,CHAR_DVLINE,CHAR_ARROW_N,CHAR_CHECKBOX_SET)])
    string = "a string"
    
    #console.init(200,120,"Root")
    #console.init(80,48,"Root")
    console.init(80,80,"Root")
    #console.set_fullscreen(True)
    root = console.canvas()
    
    #panel = AbsoluteLayout()
    
    label1 = Label("Here is some text") >> Padding(top=5) >> Border(double_line, fg_colour=white) >> Fill(bg_colour=dark_blue)
    label2 = Label("This is a really long string of text.") >> Padding(hpad=3, vpad=2) >> Border(double_line, fg_colour=yellow) >> Fill(bg_colour=dark_red)
    label3 = Label("This text is right-aligned") >> Padding(hpad=8) >> Border(single_line, fg_colour=red) >> Fill(bg_colour=dark_amber)
    label4 = Text('The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested.\n\nSections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.', 30, nbsp='s') >> Padding(hpad=2, vpad=1) >> Border(single_line, fg_colour=red) >> Fill(bg_colour=dark_amber)
    
    #label4 = Label("This is a really long string of text.") >> Padding(hpad=3, vpad=2) >> Border(double_line, fg_colour=yellow) >> Fill(bg_colour=dark_red)
    
    label1.render(root, 30, 9)
    label2.render(root, 40, 15)
    label3.render(root, 30, 4)
    label4.render(root, 10, 25)
    #panel.add(label1, 30, 9, zlevel=2)
    #panel.add(label2, 40, 15, halign="left", zlevel=3)
    #panel.add(label3, 30, 4, zlevel=1, halign="right")
    #panel.add(label4, 10, 25, halign="left", zlevel=4)
    
    bg = RectangleShape(console.width(),console.height(), char="/", fg_colour=dark_grey, bg_colour=darkest_red)
    #panel.add(bg, 0, 0, zlevel=-100)
    
    #bg.render(root,0,0)
    #panel.render(root, 0,0)
    
    #key_input.check_for_input()
    
    console.flush()
    #time.sleep(0.015)
    
    console.wait_for_user()