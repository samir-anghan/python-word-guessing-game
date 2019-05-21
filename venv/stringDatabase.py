class StringDatabase:
    """
    Responsible for all disk input/output operations.
    """
    wordsList = []

    def __init__(self, filename):
        """
        Constructs a new object and initializes the attributes of the class StringDatabase.
        :param filename: File name to read words from.
        :type filename: str
        """
        self.filename = filename
        self.read_words_from_file()

    def read_words_from_file(self):
        """
        Read words from the text file.
        :return: None
        :rtype: None
        """
        try:
            with open(self.filename, 'rU') as f:
                for line in f:
                    for word in line.split():
                        self.wordsList.append(word)
        except Exception as ex:
            print(ex)
