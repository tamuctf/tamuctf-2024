import logging
import os
import sys
from math import ceil
from math import gcd
from math import log

from sage.all import Zmod
from sage.all import is_prime

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)


def _get_possible_primes(e, d):
    logging.debug(f"Looking for possible primes for {e = }, {d = }")
    mul = e * d - 1
    for k in range(3, e):
        if mul % k == 0:
            p = (mul // k) + 1
            if is_prime(p):
                yield p


def attack(e_start, e_end, N=None, dp=None, dq=None, p_bit_length=None, q_bit_length=None):
    """
    Generates possible prime factors for a modulus, if d_p and/or d_q are known.
    More information: Campagna M., Sethi A., "Key Recovery Method for CRT Implementation of RSA"
    :param e_start: the start value of the public exponent (inclusive)
    :param e_end: the end value of the public exponent (exclusive)
    :param N: the modulus, will be used to check the factors if not None (default: None)
    :param dp: the d exponent for p, will be used to generate possible factors for p if not None (default: None)
    :param dq: the d exponent for q, will be used to generate possible factors for q if not None (default: None)
    :param p_bit_length: the bit length of p, will be used to check possible factors for p if not None (default: None)
    :param q_bit_length: the bit length of q, will be used to check possible factors for q if not None (default: None)
    :return: a generator generating tuples containing possible prime factors
    """
    assert not (dp is None and dq is None), "At least one of the CRT private exponents should be known."

    if dp is not None and dq is not None:
        for e in range(e_start, e_end, 2):
            for p in _get_possible_primes(e, dp):
                for q in _get_possible_primes(e, dq):
                    if (N is None or p * q == N) and (p_bit_length is None or p.bit_length() == p_bit_length) and (q_bit_length is None or q.bit_length() == q_bit_length):
                        yield p, q

        return None

    if dp is not None:
        for e in range(e_start, e_end, 2):
            for p in _get_possible_primes(e, dp):
                if p_bit_length is None or p.bit_length() == p_bit_length:
                    if N is None:
                        yield p
                    elif N % p == 0:
                        yield p, N // p

        return None

    if dq is not None:
        for e in range(e_start, e_end, 2):
            for q in _get_possible_primes(e, dq):
                if q_bit_length is None or q.bit_length() == q_bit_length:
                    if N is None:
                        yield q
                    elif N % q == 0:
                        yield q, N // q

        return None


N = 25738076489477390048107389684996103882556969202513166288259522036337632736404168235030854616722305580161628671792338702584031628109920559959142086244929697000719839651284769225292474824312234101039383526660410096665677108899401181859913502426847877961086164703198858818644081120668614573404426468513602005820885294275008357193783600514925643269093575426795017766522751748746504263462858714066992146006524560800527477669712171172719903914727042988942644713692028132153937805550877286612258743238152980687480412165259102950423845139742038860174525053539636028083341480124394591958643772596948645492958078465902879395979
e = 65537
dp = 50968599685318031105881460829473157194091587946843377485132132201709336331990388991811359191525203832010150564061805089532798692759984816129032217261354520135820341025684129991066636380282906041936644071267224730887914721759483881066898124618832251573208683287214270833228650694160027400718571872720918366637
dq = 59570580958029296697489034445859280417465234989467079096241379549137272725225834714245769888872900567685889790818215865253809045197303829071661146301592714381513010124144245990857167303789798604218181960500974361533549587221903516268024463379717484096159040873883611288985840958255028780220438854225482888055
p, q = next(attack(e, e + 1, N=N, dp=dp, dq=dq))
print(f"p = {p}")
print(f"q = {q}")

'''
p = 175686589048371524987437716214231436544952421988758977028512309898670634575798354986395679131909077133458646058850182514737865035891817435157438827258054551419621190227752633841294595721590533491316564587316052552895454011463277500314590143225393639686181953221172969420780838402312402869662496440462358754237
q = 146499949876031596595119473544158492278112465965128296098554215599527541093216463269448197726258519438043835011477106576649738579124758942019192335365960513430943680607378942906030476700381704046104806602324753526654817790452245515616252739559328483440653497757953778117237609624419671326102551735126101243367
'''