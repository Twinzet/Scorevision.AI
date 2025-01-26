import re
from highlight import measureNotes, checkIfPresent, readFile, highlightMeasure

textArray = []

def extractMeasureInfo(measure):
    """Analyze and extract key information from a measure of notes."""
    for line in measure:
        print(line)
        # Crescendo and Diminuendo

        # Slur
        if "(" in line or ")" in line:
            textArray.append("This measure contains a slur: Play the notes smoothly and connected.")

        # Tie
        elif "~" in line:
            textArray.append("This measure contains a tie: Play the connected notes as one.")

        # Dynamics
        if "\\ppp" in line:
            textArray.append("- ppp (pianississimo): Extremely soft.")
        elif "\\pp" in line:
            textArray.append("- pp (pianissimo): Very soft.")
        elif "\\p" in line:
            textArray.append("- p (piano): Soft.")
        elif "\\mf" in line:
            textArray.append("- mf (mezzo-forte): Moderately loud.")
        elif "\\mp" in line:
            textArray.append("- mp (mezzo-piano): Moderately soft.")
        elif "\\fff" in line:
            textArray.append("- fff (fortississimo): Extremely loud.")
        elif "\\ff" in line:
            textArray.append("- ff (fortissimo): Very loud.")
        elif "\\f" in line:
            textArray.append("- f (forte): Loud.")

        # Accidentals
        elif "es" in line:
            textArray.append("This measure contains a flat (♭).")
        elif "is" in line:
            textArray.append("This measure contains a sharp (♯).")
        elif "!" in line:
            textArray.append("This measure contains a natural (♮).")

        # Rests
        elif "r" in line:
            if "r1" in line:
                textArray.append("Whole rest: Silence for 4 beats.")
            elif "r2" in line:
                textArray.append("Half rest: Silence for 2 beats.")
            elif "r4" in line:
                textArray.append("Quarter rest: Silence for 1 beat.")
            elif "r8" in line:
                textArray.append("Eighth rest: Silence for half a beat.")
            elif "r16" in line:
                textArray.append("Sixteenth rest: Silence for a quarter of a beat.")
        
        # Dotted notes or rests
        if "." in line and "r" in line:
            textArray.append("This measure contains a dotted rest, indicating an extended duration.")

def analyzeKeySignature(measure):
    """Analyze key signature information from the LilyPond file."""
        # Dictionary to store major and minor key signatures and their notes
    major_keys = {
        "c": "C Major: C, D, E, F, G, A, B",
        "d": "D Major: D, E, F#, G, A, B, C#",
        "e": "E Major: E, F#, G#, A, B, C#, D#",
        "f": "F Major: F, G, A, Bb, C, D, E",
        "g": "G Major: G, A, B, C, D, E, F#",
        "a": "A Major: A, B, C#, D, E, F#, G#",
        "b": "B Major: B, C#, D#, E, F#, G#, A#",
        "c#": "C# Major: C#, D#, E#, F#, G#, A#, B#",
        "d#": "D# Major: D#, E#, F##, G#, A#, B#, C##",
        "f#": "F# Major: F#, G#, A#, B, C#, D#, E#",
        "g#": "G# Major: G#, A#, B#, C#, D#, E#, F##",
        "a#": "A# Major: A#, B#, C##, D#, E#, F##, G#"
    }


    minor_keys = {
        "a": "A Minor: A, B, C, D, E, F, G",
        "b": "B Minor: B, C#, D, E, F#, G, A",
        "c": "C Minor: C, D, Eb, F, G, Ab, Bb",
        "d": "D Minor: D, E, F, G, A, Bb, C",
        "e": "E Minor: E, F#, G, A, B, C, D",
        "f": "F Minor: F, G, Ab, Bb, C, Db, Eb",
        "g": "G Minor: G, A, Bb, C, D, Eb, F",
        "a#": "A# Minor: A#, B, C#, D#, E, F#, G#",
        "c#": "C# Minor: C#, D#, E, F#, G#, A, B",
        "d#": "D# Minor: D#, E#, F#, G#, A#, B, C#",
        "f#": "F# Minor: F#, G#, A, B, C#, D, E",
        "g#": "G# Minor: G#, A#, B, C#, D#, E, F#"
    }

    if "\\key" in measure:
        key = measure.split("\\key")[1].split()[0].strip()
        mode = measure.split("\\key")[1].split()[1].strip()

        if mode == "\\major" and key in major_keys:
            textArray.append(major_keys[key])
        elif mode == "\\minor" and key in minor_keys:
            textArray.append(minor_keys[key])
        else:
            textArray.append("Unknown key or mode.")

def extractTimeSignature(measure):
    timeSignatures = []
    # Regular expression to find the time signature (e.g., \time 4/4)
    pattern = r'\\time (\d+/\d+)'
   
    for line in measure:
        matches = re.findall(pattern, line)
        if matches != None:
            for match in matches:
              timeSignatures.append(match)

    # Append the found time signatures to the list
   
    time_signature_description(timeSignatures)


# Function to print the description and tips based on the time signature
def time_signature_description(timeSignature):
    if timeSignature == "4/4":
        textArray.append("4/4 Time (Common Time)")
        textArray.append("Description: This is the most commonly used time signature in Western music. The top number indicates 4 beats per measure, and the bottom number indicates that a quarter note gets one beat.")
        textArray.append("Feeling: Strong, regular, easy to count. The pulse feels steady and balanced.")
        textArray.append("Tips for Playing:")
        textArray.append("- Emphasize beats: In 4/4, beat 1 is often the strongest, followed by beats 2, 3, and 4 with progressively lighter emphasis.")
        textArray.append("- Count '1-2-3-4': You can tap or count '1-2-3-4' for every measure, making sure each beat is evenly spaced.")
        textArray.append("- Use the backbeat: In many genres (especially pop and rock), beats 2 and 4 are emphasized in the percussion, creating a 'backbeat' feel.")
       
    elif timeSignature == "3/4":
        textArray.append("3/4 Time (Waltz Time)")
        textArray.append("Description: This time signature has 3 beats per measure, with the quarter note receiving one beat.")
        textArray.append("Feeling: The rhythm often feels like a 'waltz,' where the first beat is accented, and the second and third beats are softer.")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3': Emphasize the first beat ('1') of each measure for a strong downbeat, and count '2' and '3' softly.")
        textArray.append("- Strong-weak-weak pattern: Think of the pattern as a 'strong-weak-weak' feel, with the first beat as the heaviest.")
        textArray.append("- Flowing motion: In waltz music, there’s often a smooth, flowing quality, so keep the movement of the hand and foot light.")
       
    elif timeSignature == "2/4":
        textArray.append("2/4 Time")
        textArray.append("Description: This time signature has 2 beats per measure, and the quarter note gets one beat.")
        textArray.append("Feeling: Very straightforward and march-like. It’s often used in marches, polkas, and quick, driving pieces.")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2': Emphasize the first beat ('1') in each measure.")
        textArray.append("- Marching feel: Think of a march, where the beat is quick and steady, and you move from one beat to the next with no pause.")
        textArray.append("- Quick tempo: Pieces in 2/4 are often faster, so practice playing cleanly with energy, focusing on evenness.")
       
    elif timeSignature == "6/8":
        textArray.append("6/8 Time")
        textArray.append("Description: There are 6 beats per measure, and the eighth note receives one beat.")
        textArray.append("Feeling: This time signature is typically grouped in two main beats of 3 eighth notes each (often described as '1-2-3, 4-5-6').")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3, 4-5-6': Emphasize the first beat of each group of three. So, you’ll feel two 'pulses' per measure (with each pulse containing three notes).")
        textArray.append("- Lilt or swing: Often used in compound meters like this, the rhythm has a 'lilt' or swing, creating a rolling feel.")
        textArray.append("- Subdivide: When practicing, think of each set of 3 eighth notes as one group and focus on bringing out the downbeats (1 and 4).")
       
    elif timeSignature == "5/4":
        textArray.append("5/4 Time")
        textArray.append("Description: This time signature has 5 beats per measure, and the quarter note gets one beat.")
        textArray.append("Feeling: It’s an odd time signature and can feel uneven, with the beats grouped in either 3 + 2 or 2 + 3 patterns.")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3-4-5': In this case, the accents can either be in groups of 3 + 2 or 2 + 3, depending on the music.")
        textArray.append("- Feel the phrasing: Sometimes, 5/4 is split into 3 beats followed by 2 beats or the reverse. Identify which grouping is being used and practice the phrasing that way.")
        textArray.append("- Flexibility: Because it’s an irregular time signature, the rhythm will often shift or feel a bit more free-form. Focus on the pulse and flow of the piece.")
       
    elif timeSignature == "7/8":
        textArray.append("7/8 Time")
        textArray.append("Description: This time signature has 7 beats per measure, and the eighth note gets one beat.")
        textArray.append("Feeling: It’s another odd time signature, often split into 3 + 2 + 2 or 2 + 3 + 2 groupings.")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3-4-5-6-7': Depending on the piece, you may divide the measure into groups of 2s and 3s (either 3+2+2 or 2+3+2).")
        textArray.append("- Accent pattern: In many pieces, the accents will fall on the first note of each group (either on the 1st, 4th, or 6th beats).")
        textArray.append("- Subdivide: As with other irregular time signatures, subdivide the beats and practice each hand independently.")
       
    elif timeSignature == "9/8":
        textArray.append("9/8 Time")
        textArray.append("Description: In this time signature, there are 9 beats per measure, and the eighth note gets one beat.")
        textArray.append("Feeling: It’s a compound time signature, usually grouped in 3 groups of 3 beats (1-2-3, 4-5-6, 7-8-9).")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3, 4-5-6, 7-8-9': The feeling is typically divided into three groups of three eighth notes. Practice counting each group and then bringing them together as a cohesive pulse.")
        textArray.append("- Smooth and flowing: It often feels like a smooth, rolling motion, with emphasis on the first note of each group.")
        textArray.append("- Balance groups: Each group of three should be evenly spaced, with no part dragging or rushing.")
       
    elif timeSignature == "12/8":
        textArray.append("12/8 Time")
        textArray.append("Description: There are 12 beats per measure, with the eighth note getting one beat.")
        textArray.append("Feeling: It’s a compound time signature, often grouped in 4 sets of 3 beats (1-2-3, 4-5-6, 7-8-9, 10-11-12).")
        textArray.append("Tips for Playing:")
        textArray.append("- Count '1-2-3, 4-5-6, 7-8-9, 10-11-12': The pulse is divided into 4 groups of 3, each accented on the first note of each group.")
        textArray.append("- Lilt and swing: The rhythm should feel flowing and rolling, often with a swing feel.")
        textArray.append("- Practice slowly: Due to the faster tempo typically associated with 12/8, practice slowly and focus on maintaining evenness across all groups.")


def lineOut(measures):
    extractMeasureInfo(measures)
    analyzeKeySignature(measures)
    extractTimeSignature(measures)


def parseMeasures(fileName, startMeasure):
    # Extract the measures using measureNotes
    fileName = fileName + ".ly"
    measures = measureNotes(startMeasure, fileName)

    print(f"Analyzing Measure {startMeasure}:\n")
    
    # Analyze each line within the extracted measure(s)
    for line in measures:
        if line == "Break":
            print("\n--- End of Measure ---\n")
            continue

    lineOut(measures)

def accessJ(fileName,measure):
    parseMeasures(fileName,measure)
    res = []
    [res.append(val) for val in textArray if val not in res]
    return res
