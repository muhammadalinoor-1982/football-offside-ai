def determine_offside(
    attackers,
    defenders
):

    if len(attackers) == 0:
        return "NO_ATTACKER"

    if len(defenders) < 2:
        return "UNKNOWN"

    defenders = sorted(
        defenders,
        key=lambda d: d["x"]
    )

    second_last_defender = defenders[-2]

    for attacker in attackers:

        if attacker["x"] > second_last_defender["x"]:

            return "OFFSIDE"

    return "ONSIDE"


