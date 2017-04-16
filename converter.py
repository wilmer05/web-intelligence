import constants
def convert_url(file_name):
    tmp = file_name.split("//")[0]
    file_name = file_name.split("//")[1]
    if file_name is None or len(file_name) == 0:
        return None
    if file_name[-1] != "/":
        file_name += "/"
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("/", "_")
    hashed = hash(file_name) % constants.HASH_SIZE
    dir_name = "descargas/" + str(hashed) + "/"
    file_name = dir_name +  file_name + ".txt"
    return dir_name, file_name
