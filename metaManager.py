class metaManager:

    @staticmethod
    def write_to_meta(filename, url):
        with open("log/meta", mode='a') as file:
            file.write(filename + " " + url)
            file.write("\n")

    @staticmethod
    def read_meta(filename):
        with open("log/meta", mode='r') as file:
            for line in file:
                key = line.split(" ")[0]
                value = line.split(" ")[1]
                if key == filename:
                    return value
    
