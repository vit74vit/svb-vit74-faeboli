class QuadEnc(Module,AutoCSR):
    def __init__(self, pads):
        self.pads = pads
        #physical pads
        a=Signal() #input A
        b=Signal() #input B
        
        #register outputs
        self.out=Signal(32) #counter output
        #register inputs
        self.reset=Signal(1) #reset counter
        self.enable=Signal(1) #enable counter
        #Internal signals
        syncr=Signal(2) #Syncronization register
        AB=Signal(2) #Syncronization register
        os=Signal(2) #old state
        ns=Signal(2) #new state
        tmp=Signal(2) #

        self.comb += a.eq(pads.A)
        self.comb += b.eq(pads.B)
        self.sync+=If(self.enable==1,              # first syncronizer
        syncr.eq(Cat(a,b))) 
        self.sync+=AB.eq(syncr)                      # second syncronizer
        self.comb+=tmp.eq(Cat(AB[1]^AB[0],AB[1]))
        self.comb+=ns.eq(tmp-os)
        self.sync+=If(ns[0]==1,(os.eq(os+ns)),(If(ns[1]==1,self.out.eq(self.out-1)).Else(self.out.eq(self.out+1))))
        self.sync+=If(self.reset==1,
        self.out.eq(0))
