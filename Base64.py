import base64

# data = open("base64.txt", "r").read()
data = open("/Users/trav/Desktop/Python/ARSCAN/PLY_Files/Riddy.ply", "r").read()
encoded = base64.b64encode(data)
decoded = base64.b64decode(encoded)
print (encoded)

print("hELLO")

print (decoded)
