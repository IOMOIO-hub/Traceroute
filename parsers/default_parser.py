from response import Response


class DefaultParser:
    def parse(self, data):
        desc, country, a_system = "", "", ""
        for line in data.splitlines():
            temp = line.split(":")
            if temp[0] == "descr" and temp[1].strip() != "":
                desc = temp[1].strip()
            elif temp[0] == "country" and temp[1].strip() != "":
                country = temp[1].strip()
            elif temp[0] == "origin" and temp[1].strip() != "":
                a_system = temp[1].strip()
        return Response(a_system, desc, country)
