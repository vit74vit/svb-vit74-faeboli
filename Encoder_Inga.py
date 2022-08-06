class QuadEnc(Module,AutoCSR):
    def __init__(self, pads):
        self.pads = pads
        W = 14
        self._out=CSRStorage(size=2*W, description="Encoders", write_from_dev=True)
        A = Signal(1)
        B = Signal(1)
        Z = Signal(1)
        zr = Signal(1)
        c = Signal(W - 1)
        i = Signal(W - 1)
        zl = Signal(1)
        out = Signal(2 * W)
        Ad = Signal(3)
        Bd = Signal(3)
        Zc = Signal(3)
        good_zero = Signal(1)
        good_one = Signal(1)
        last_good = Signal(1)
        index_pulse = Signal(1)
        count_direction = Signal(1)
        count_enable = Signal(1)
        ###
        self.comb += A.eq(pads.A)
        self.comb += B.eq(pads.B)
        self.comb += Z.eq(pads.Z)

        self.comb += out.eq(Cat(zl, i, c))
        self.sync += [
            Ad.eq(Cat(Ad[0:1], A)),
            Bd.eq(Cat(Bd[0:1], B))
        ]
        self.comb += [
            good_one.eq(Zc[2] & Zc[1] & Zc[0])
        ]
        self.comb += [
            self._out.dat_w.eq(out),
            self._out.we.eq(True)
        ]


        self.comb += [
            good_zero.eq(~(Zc[2] | Zc[1] | Zc[0]))
        ]
        self.comb += [
            index_pulse.eq(good_one & ~last_good),
            count_enable.eq(Ad[1] ^ Ad[2] ^ Bd[1] ^ Bd[2]),
            count_direction.eq(Ad[1] ^ Bd[2])
        ]
        self.sync += [
            If(Z & ~good_one,
               Zc.eq(Zc + 1)
               ).Elif(~good_zero,
                      Zc.eq(Zc - 1)
                      ),
            If(good_one,
               last_good.eq(1)
               ).Elif(good_zero,
                      last_good.eq(0)
                      ),
            If(count_enable,
               If(count_direction,
                  c.eq(c + 1)
                  ).Else(
                   c.eq(c - 1)
               )
               ),
            If(index_pulse,
               i.eq(c),
               zl.eq(1)
               ).Elif(zr,
                      zl.eq(0)
                      )
        ]
