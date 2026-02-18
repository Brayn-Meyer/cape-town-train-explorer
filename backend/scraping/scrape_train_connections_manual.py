import json

def generate_id(name):
    return name.lower().replace(" ", "_").replace("'", "").replace("-", "_")

def append_unique(items, value):
    if value not in items:
        items.append(value)

def build_graph(lines):
    graph = {}
    for line in lines:
        for i, station in enumerate(line):
            sid = station
            if sid not in graph:
                graph[sid] = {"id": sid, "front": [], "rear": []}
            if i < len(line) - 1:
                append_unique(graph[sid]["front"], line[i+1])
            if i > 0:
                append_unique(graph[sid]["rear"], line[i-1])
    return graph

def main():
    # Manual station lists for Cape Town commuter corridors
    cape_town_to_salt_river = [
        "cape_town","woodstock","salt_river"]
    salt_river_to_simons_town = [
        "salt_river","observatory","mowbray","rosebank","rondebosch",
        "newlands","claremont","harfield_road","kenilworth","wynberg","wittebome","plumstead",
        "steurhof","diep_river","heathfield","retreat","steenberg","lakeside","false_bay","muizenberg",
        "st_james","kalk_bay","fish_hoek","sunny_cove","glencairn","simons_town"
    ]

    salt_river_to_maitland = [
        "salt_river","koeberg_road","maitland"]
    
    maitland_to_retreat = [
        "maitland","ndabeni","pinelands","hazendal","athlone","crawford","lansdowne","wetton",
        "ottery","southfield","heathfield","retreat"
    ]

    maitland_to_bellville = [
        "maitland","woltemade","thornton","goodwood", "vasco", "elsies_river", "parow", "tygerberg", "bellville"
    ]

    bellville_to_eerste_river = [
        "bellville","kuils_river","blackheath","melton_rose","eerste_river"
    ]

    eerste_river_to_muldersvlei = [
        "eerste_river","lynedoch","spier","vlottenburg","stellenbosch","du_toit","koelenhof","muldersvlei" 
    ]

    cape_town_to_bellville = [
        "cape_town","esplanade","paarden_eiland","ysterplaat","kentemade","century_city","acacia_park",
        "monte_vista","de_grendel","avondale","oosterzee","bellville"
    ]
    bellville_to_muldersvlei = [
        "bellville","stikland","brackenfell","eikenfontein","kraaifontein","muldersvlei"
    ]

    eerste_river_to_strand = [
        "eerste_river","faure","firgrove","somerset_west","van_der_stel","strand"
    ]

    maitland_to_bonteheuwel = [
        "maitland","mutual","langa","bonteheuwel"
    ]

    bonteheuwel_to_bellville = [
        "bonteheuwel","lavistown","belhar","unibell","pentech","sarepta","bellville"
    ]

    bonteheuwel_to_philippi = [
        "bonteheuwel","netreg","heideveld","nyanga","philippi"
    ]

    philippi_to_khayelitsha = [
        "philippi","stock_road","mandalay","nolungile","nonkqubela","khayelitsha","kuyasa","chris_hani"
    ]

    philippi_to_kapteinsklip = [
        "philippi","lentegeur","mitchells_plain","kapteinsklip_station"
    ]

    muldersvlei_to_wellington = [
        "muldersvlei","klapmuts","paarl","huguenot","dal_josafat","mbekweni","wellington"
    ]

    # northern_line_muldersvlei = [
    #     "bellville","kuils_river","blackheath","melton_rose","eerste_river","lynedoch","spier",
    #     "vlottenburg","stellenbosch","du_toit","koelenhof","muldersvlei"
    # ]

    # northern_line_strand = [
    #     "bellville","kuils_river","blackheath","melton_rose","eerste_river","faure","firgrove",
    #     "somerset_west","van_der_stel","strand"
    # ]

    # northern_line_bellvile = [
    #     "cape_town","woodstock","salt_river","koeberg_road","maitland","maitland","woltemade","thornton",
    #     "goodwood","vasco","elsies_river","parow","tygerberg","bellville"
    # ]

    # central_line_khayelitsha = [
    #     "cape_town","woodstock","salt_river","maitland","mutual","langa","bonteheuwel","netreg","heideveld",
    #     "nyanga","philippi","stock_road","mandalay","nolungile","nonkqubela","khayelitsha","kuyasa","chris_hani"
    # ]

    # central_line_kapteinsklip = [
    #     "cape_town","woodstock","salt_river","koeberg_road","maitland","mutual","langa","bonteheuwel","netreg","heideveld",
    #     "nyanga","philippi","lentegeur","mitchells_plain","kapteinsklip_station"
    # ]

    # central_line_bellville = [
    #     "cape_town","woodstock","salt_river","koeberg_road","maitland","mutual","langa","bonteheuwel","lavistown","belhar",
    #     "unibell","pentech","sarepta","bellville"
    # ]

    # Combine all lines
    lines = [
        cape_town_to_salt_river,
        salt_river_to_simons_town,
        salt_river_to_maitland,
        maitland_to_retreat,
        maitland_to_bellville,
        bellville_to_eerste_river,
        eerste_river_to_muldersvlei,
        cape_town_to_bellville,
        bellville_to_muldersvlei,
        eerste_river_to_strand,
        maitland_to_bonteheuwel,
        bonteheuwel_to_bellville,
        bonteheuwel_to_philippi,
        philippi_to_khayelitsha,
        philippi_to_kapteinsklip,
        muldersvlei_to_wellington
    ]

    graph = build_graph(lines)

    with open("stations_graph.json", "w", encoding="utf-8") as f:
        json.dump(list(graph.values()), f, indent=2)

    print("Graph saved to stations_graph.json")

if __name__ == "__main__":
    main()
