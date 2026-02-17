import json

def generate_id(name):
    return name.lower().replace(" ", "_").replace("'", "").replace("-", "_")

def build_graph(lines):
    graph = {}
    for line in lines:
        for i, station in enumerate(line):
            sid = generate_id(station)
            if sid not in graph:
                graph[sid] = {"id": sid, "front": [], "rear": []}
            if i < len(line) - 1:
                graph[sid]["front"].append(generate_id(line[i+1]))
            if i > 0:
                graph[sid]["rear"].append(generate_id(line[i-1]))
    return graph

def main():
    # Manual station lists for Cape Town commuter corridors

    southern_line = [
        "Cape Town","Woodstock","Salt River","Observatory","Mowbray","Rosebank","Rondebosch",
        "Newlands","Claremont","Harfield Road","Kenilworth","Wynberg","Wittebome","Plumstead",
        "Steurhof","Diep River","Heathfield","Retreat","Lakeside","False Bay","Muizenberg",
        "St James","Kalk Bay","Fish Hoek","Sunny Cove","Glencairn","Simon's Town"
    ]

    cape_flats_line = [
        "Cape Town","Woodstock","Salt River","Maitland","Langa","Pinelands","Hazendal",
        "Athlone","Crawford","Lansdowne","Wetton","Ottery","Southfield","Retreat"
    ]

    northern_line_wellington = [
        "Cape Town","Woodstock","Salt River","Maitland","Ysterplaat","Century City","Goodwood",
        "Vasco","Parow","Tygerberg","Bellville","Kraaifontein","Klapmuts","Paarl","Huguenot","Wellington"
    ]

    northern_line_stellenbosch = [
        "Bellville","Kuils River","Blackheath","Melton Rose","Eersterivier","Faure","Firgrove",
        "Somerset West","Stellenbosch"
    ]

    northern_line_strand = [
        "Bellville","Kuils River","Blackheath","Melton Rose","Eersterivier","Faure","Firgrove",
        "Somerset West","Strand"
    ]

    central_line_khayelitsha = [
        "Cape Town","Woodstock","Salt River","Maitland","Langa","Bonteheuwel","Netreg",
        "Nyanga","Philippi","Stock Road","Nolungile","Nonkqubela","Khayelitsha (Chris Hani)"
    ]

    central_line_kapteinsklip = [
        "Cape Town","Woodstock","Salt River","Maitland","Langa","Bonteheuwel","Netreg",
        "Nyanga","Philippi","Stock Road","Kapteinsklip"
    ]

    central_line_bellville = [
        "Cape Town","Woodstock","Salt River","Maitland","Ysterplaat","Century City","Goodwood",
        "Vasco","Parow","Tygerberg","Bellville"
    ]

    # Combine all lines
    lines = [
        southern_line,
        cape_flats_line,
        northern_line_wellington,
        northern_line_stellenbosch,
        northern_line_strand,
        central_line_khayelitsha,
        central_line_kapteinsklip,
        central_line_bellville
    ]

    graph = build_graph(lines)

    with open("stations_graph.json", "w", encoding="utf-8") as f:
        json.dump(list(graph.values()), f, indent=2)

    print("Graph saved to stations_graph.json")

if __name__ == "__main__":
    main()
