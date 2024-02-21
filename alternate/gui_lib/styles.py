
def set_styles(s):
    # s.element_options('Button.label')
    print(s.element_options('Button.label'))
    

    s.configure('Header.TLabel', font=('bell',20), padding=(5,10,5,0))
    s.configure('HeaderRed.TLabel', font=('bell',20), padding=(5,5,5,5), foreground="red")
    s.configure('HeaderGreen.TLabel', font=('bell',20), padding=(5,5,5,5), foreground="green")
    s.configure('Display.TLabel', font=('bell',16),padding=(5,20,5,20))
    s.configure('Display2.TLabel', font=('bell',16),padding=(5,10,5,10))
    s.configure('DisplayInner.TLabel', font=('bell',16), padding=(5,10,5,10))
    
    #s.configure('Display.TFrame', borderwidth=2, relief="raised")
    #s.configure('Display.TLabelframe', font=('bell',16), padding=(5,20,5,20), relief="flat", borderwidth=2)
    
    


