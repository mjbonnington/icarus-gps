import os, sys
os.environ['IC_ENV'] = 'CLARISSE'
sys.path.append('/Users/Kikos/Work/GPS/pipeline__dev__/icarus/ui')
import icarus__main__; reload(icarus__main__)