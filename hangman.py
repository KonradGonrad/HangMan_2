
stage1 = """        \n
        \n
        \n
        \n
        \n
________\n
"""

stage2 = """        \n
|       \n
|       \n
|       \n
|       \n
________\n
"""

stage3 = """______  \n
|       \n
|       \n
|       \n
|       \n
________\n
"""

stage4 = """______  \n
|    |  \n
|       \n
|       \n
|       \n
________\n
"""

stage5 = """______  \n
|    |  \n
|    0  \n
|       \n
|       \n
________\n
"""

stage6 = """______  \n
|    |  \n
|    0  \n
|    |  \n
|       \n
________\n
"""


stage7 = """______  \n
|    |  \n
|    0  \n
|   /|  \n
|       \n
________\n
"""

stage8 = """______  \n
|    |  \n
|    0  \n
|   /|\ \n
|       \n
________\n
"""

stage9 = """______  \n
|    |  \n
|    0  \n
|   /|\ \n
|   /   \n
________\n
"""

stage10 = """______  \n
|    |  \n
|    0  \n
|   /|\ \n
|   / \ \n
________\n
"""

stages = {"stage1":stage1,
           "stage2":stage2,
           "stage3":stage3,
           "stage4":stage4,
           "stage5":stage5,
           "stage6":stage6,
           "stage7":stage7,
           "stage8":stage8,
           "stage9":stage9,
           "stage10":stage10}

def hangman_stage(i: int):
    stage = f"stage{i}"
    return stages[stage]

if __name__ == "__main__":
    print(hangman_stage(10))

    