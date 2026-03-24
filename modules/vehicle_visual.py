def status_color(status):

    if status == "OK":
        return "🟢"

    elif status == "WARNING":
        return "🟡"

    else:
        return "🔴"


def render_vehicle(row):

    depan = status_color(row["BODY_DEPAN"])
    kanan = status_color(row["BODY_KANAN"])
    kiri = status_color(row["BODY_KIRI"])
    belakang = status_color(row["BODY_BELAKANG"])

    diagram = f"""

            DEPAN
            {depan}

    {kiri}          {kanan}

            {belakang}
           BELAKANG

    """

    return diagram