from rpy2.robjects import *
from rpy2.robjects.vectors import DataFrame
from rpy2.robjects.packages import importr
import rpy2.robjects.lib.ggplot2 as ggplot2
from InputConvert import GroupConvert

excel = importr('readxl')
ropls = importr('ropls')
r_base = importr('base')
grDevices = importr('grDevices')
gridExtra = importr('gridExtra')

class Data:
    def __init__(self, raw_data=None, numeric_data=None, metadata=None, specified_numeric_data=None, specified_metadata=None, file_name=None):
        self.raw_data = raw_data
        self.numeric_data = numeric_data
        self.metadata = metadata
        self.specified_numeric_data = specified_numeric_data
        self.specified_metadata = specified_metadata
        self.file_name = file_name
        self.metabolite_dict = {}

    def read_data(self, file_name, col_from, col_to):
        RawData = DataFrame(excel.read_excel("../Data/"+file_name+'.xlsx'))
        NumericData = RawData.rx(True, IntVector(range(col_from, col_to + 1)))
        MetaData = RawData.rx(True, col_from-1)[0]
        RawData._set_rownames(IntVector(range(1,len(MetaData)+1)))
        self.file_name = file_name
        self.raw_data = RawData
        #print(self.raw_data)
        self.numeric_data = NumericData
        self.metadata = r_base.factor(MetaData)
        self.metadata_list = list(MetaData)
        self.metabolite_list = list(self.raw_data.names)[1:]
        self.make_metabolite_dict()

    def select_data(self, groups):
        #print(IntVector(GroupConvert(groups,self.metadata_list)), IntVector(range(6)))
        self.specified_numeric_data = self.numeric_data.rx(StrVector(GroupConvert(groups,self.metadata_list)),True)
        print(self.specified_numeric_data)
        self.specified_metadata = r_base.factor(self.metadata.rx(IntVector(GroupConvert(groups,self.metadata_list))))

    def PCA(self, color):
        r('graphics.off()')
        if len(self.metadata) >= 7:
            CrossValI = 7
        else:
            CrossValI = len(self.metadata)
        pca = ropls.opls(self.numeric_data, crossvalI=CrossValI, predI=2)
        r('graphics.off()')
        try:
            grDevices.X11()
            ropls.plot(pca,
                       typeVc="x-loading",
                       parCexN=1)

            grDevices.X11()
            ropls.plot(pca,
                       typeVc="x-score",
                       parAsColFcVn=self.metadata,
                       parLabVc=StrVector(r_base.rep("●", len(self.metadata))),
                       parPaletteVc=StrVector(color),
                       parCexN=1)
        except:
            pass

    def PLS(self, color):
        r('graphics.off()')
        if len(self.specified_metadata) >= 7:
            CrossValI = 7
        else:
            CrossValI = len(self.specified_metadata)
        opls = ropls.opls(self.specified_numeric_data, self.specified_metadata, crossvalI=CrossValI, predI=2)
        r('graphics.off()')
        try:
            grDevices.X11()
            ropls.plot(opls,
                       typeVc="x-loading",
                       parCexN=1)

            grDevices.X11()
            ropls.plot(opls,
                       typeVc="x-score",
                       parAsColFcVn=self.specified_metadata,
                       parLabVc=StrVector(r_base.rep("●", len(self.specified_metadata))),
                       parPaletteVc=StrVector(color),
                       parCexN=1)
        except:
            pass

    def OPLS(self, color):
        r('graphics.off()')
        if len(self.specified_metadata) >= 7:
            CrossValI = 7
        else:
            CrossValI = len(self.specified_metadata)
        opls = ropls.opls(self.specified_numeric_data, self.specified_metadata, crossvalI=CrossValI, predI=1, ortho=r('NA'))
        r('graphics.off()')
        try:
            grDevices.X11()
            ropls.plot(opls,
                       typeVc="x-loading",
                       parCexN=1)

            grDevices.X11()
            ropls.plot(opls,
                       typeVc="x-score",
                       parAsColFcVn=self.specified_metadata,
                       parLabVc=StrVector(r_base.rep("●", len(self.specified_metadata))),
                       parPaletteVc=StrVector(color),
                       parCexN=1)
        except:
            pass

    def BoxPlot_One(self, metabolite):
        #print(self.raw_data)
        r('graphics.off()')
        gp = ggplot2.ggplot(self.raw_data)
        pp = gp + \
            ggplot2.aes_string(x=self.metadata, y='`'+self.metabolite_dict[metabolite]+'`') + \
            ggplot2.geom_boxplot()
        pp.plot()

    def make_metabolite_dict(self):
        for i in range(len(self.metabolite_list)):
            self.metabolite_dict[self.metabolite_list[i]]=str(i+1)
        self.raw_data._set_colnames(StrVector(range(len(self.metabolite_list)+1)))
        #print(self.metabolite_dict)

    def BoxPlot_All(self):
        #print(self.metabolite_list)
        r('graphics.off()')
        plots = []
        for i in range(1,len(self.metabolite_list)+1):
            if i%4==0 and i>0:
                grDevices.X11()
                gridExtra.grid_arrange(*plots, nrow=2,ncol=2)
                plots = []

            gp = ggplot2.ggplot(self.raw_data)
            plots.append(gp + \
                 ggplot2.aes_string(x=self.metadata, y='`'+str(i)+'`') + \
                 ggplot2.geom_boxplot())

        grDevices.X11()
        gridExtra.grid_arrange(*plots, nrow=2, ncol=2)









