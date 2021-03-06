import datetime

import pycitrus

p = pycitrus.CitrusProcessor(740.3e6, 10e6)
p.init("lime")
out = p.run()

name = "{:%Y-%m-%d-%H-%M-%S}".format(datetime.datetime.now())
with open(f'pycitrus_data/output_{name}.txt', "w") as f:
    for item in out:
        f.write(str(item) + '\n')

p.close()
