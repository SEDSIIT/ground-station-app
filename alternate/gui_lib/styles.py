
def set_styles(s):
    # s.element_options('Button.label')
    print(s.element_options('Button.label'))
    

    s.configure('Header.TLabel', font=('bell',24), padding=(5,10,5,20))
    s.configure('Display.TLabel', font=('bell',16),padding=(5,20,5,20))
    s.configure('DisplayInner.TLabel', font=('bell',16), padding=(5,10,5,10))
    #s.configure('Display.TFrame', borderwidth=2, relief="raised")
    #s.configure('Display.TLabelframe', font=('bell',16), padding=(5,20,5,20), relief="flat", borderwidth=2)
    
    


