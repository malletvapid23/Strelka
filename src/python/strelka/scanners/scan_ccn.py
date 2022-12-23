import re

from strelka import strelka


class ScanCcn(strelka.Scanner):
    """Decodes base64-encoded file."""

    def luhn_checksum(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def is_luhn_valid(self, card_number):
        return self.luhn_checksum(card_number) == 0

    def scan(self, data, file, options, expire_at):
        re_visa = re.compile(rb"4[0-9]{12}(?:[0-9]{3})?")

        if matches := re_visa.findall(data):
            for match in matches:
                try:
                    if self.is_luhn_valid(match.decode("ascii")):
                        if "luhn_match" not in self.flags:
                            self.flags.append("luhn_match")
                except:
                    pass
