class keyInfo:
    # 類的初始化方法，用來設置對象的屬性
    def __init__(
        self,
        keyName,
        textLU,
        textLD,
        textRU,
        textRD,
        keyLUSize=0.3,
        keyLDSize=0.3,
        keyRUSize=0.3,
        keyRDSize=0.3,
    ):
        self.keyName = keyName
        self.textLU = textLU
        self.textLD = textLD
        self.textRU = textRU
        self.textRD = textRD
        self.keyLUSize = keyLUSize
        self.keyLDSize = keyLDSize
        self.keyRUSize = keyRUSize
        self.keyRDSize = keyRDSize
