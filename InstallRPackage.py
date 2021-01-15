from rpy2.robjects import*
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

def install_package():
    #you must run this as root
    packnames = ('readxl', 'BiocManager','ggplot2','gridExtra')
    if all(rpackages.isinstalled(x) for x in packnames):
        have_packages = True

    else:
        have_packages = False

    if not have_packages:
        utils = rpackages.importr('utils')
        utils.chooseCRANmirror(ind=1)

        packnames_to_install = [x for x in packnames if not rpackages.isinstalled(x)]

        if len(packnames_to_install) > 0:
            utils.install_packages(StrVector(packnames_to_install))

    r('BiocManager::install("ropls")')

install_package()
