import SoapySDR

# enumerate devices
results = SoapySDR.Device.enumerate()
for result in results:
    print(result)

# create device instance
# args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)
settings = {
    s.key: {'value': s.value, 'name': s.name, 'description': s.description}
    for s in sdr.getSettingInfo()
}
print(settings)
