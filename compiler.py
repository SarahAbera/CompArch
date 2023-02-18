from py_parser import *
from typing import List, Dict


class TemporaryMarker:
    def __init__(self, default, alt, label):
        self.value = default
        self.alt_value = alt
        self.label = label

    def __str__(self):
        return self.value


class Block:
    def __init__(self, data_segment, var_counter, marker_stack):
        self.child = []

        # initialized by compiler and passed to every block to sync label names
        self.data_segment: Dict = data_segment
        self.var_counter: Dict = var_counter
        self.markers_stack: List = marker_stack

    def __repr__(self):
        return str(self.child)

    def recreate(self, depth=0):
        for child in self.child:
            if isinstance(child, str):
                yield (depth, child)
            else:
                yield from child.recreate(depth + 1)

    def print_int(self, num):
        return f"li $a0, {num}\nli $v0, 1\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def print_var_int(self, var):
        return f"lw $a0, {var}\nli $v0, 1\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def print_var_str(self, var):
        return f"la $a0, {var}\nli $v0, 4\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def input(self, dest):
        return f"li $a0, {dest}\n\nli $v0, 1\nsyscall\n"

    def add(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

    def sub(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

    def mul(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

    def div(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

    def beq(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbeq $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbeq $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbeq $t0, $t1, {dest}\n"

    def bne(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbne $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbne $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbne $t0, $t1, {dest}\n"

    def blt(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nblt $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nblt $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nblt $t0, $t1, {dest}\n"

    def bgt(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbgt $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbgt $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbgt $t0, $t1, {dest}\n"

    def ble(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nble $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nble $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nble $t0, $t1, {dest}\n"

    def bge(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbge $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbge $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbge $t0, $t1, {dest}\n"

    def assign(self, exp, dest):
        if len(exp) == 1:
            value = exp[0]
            if value == "input":
                raise Exception("unsuppotred")
            if isinstance(value, int):
                if dest not in self.data_segment:
                    self.data_segment[dest] = value
                return f"li $t0, {value}\nsw $t0, {dest}\n"

            elif isinstance(value, str):
                if value[0] in ["'", '"']:  # actual str
                    self.data_segment[dest] = value[1:-1]

                else:  # variable
                    if dest not in self.data_segment:
                        self.data_segment[dest] = 0
                    return f"lw $t0, {value}\nsw $t0, {dest}\n"

        elif len(exp) == 2:
            preamble = ""
            arg = exp[1]
            print_ = f"print({arg})"
            preamble = self.to_mips(print_)

            take_input = f"la $a0, {dest}\nli $a1, 20\nli $v0, 8\nsyscall\n"
            if dest not in self.data_segment:
                self.data_segment[dest] = " " * 20
            return preamble + take_input

        elif len(exp) == 3:
            ops = {"+": "add", "-": "sub", "*": "mul", "/": "div"}

            op1, op, op2 = exp

            if dest not in self.data_segment:
                self.data_segment[dest] = 0

            if isinstance(op1, int) and isinstance(op2, int):
                return self.assign([int(eval("".join(map(str, exp))))], dest)

            else:
                operation = self.__getattribute__(ops.get(op))
                return operation(op1, op2, dest)

        return ""

    def for_loop(self, start, end, step, loop_variable):
        load_start = f"lw $t7, {loop_variable}"

        if isinstance(end, int):
            load_end = f"li $t8, {end}"
        else:
            load_end = f"lw $t8, {end}"

        if isinstance(step, int):
            load_step = f"li $t9, {step}"
        else:
            load_step = f"lw $t9, {step}"

        end_loop = f"end_loop_{self.var_counter['loop']}"

        before = f"""

{self.assign([start], loop_variable)}
{load_start}
{load_end}
{load_step}

loop_{self.var_counter['loop']}:

blt $t9, $zero, decreasing_{self.var_counter['loop']}
bge $t7, $t8, {end_loop}
j end_guard_{self.var_counter['loop']}

decreasing_{self.var_counter['loop']}:
ble $t7, $t8, {end_loop}
end_guard_{self.var_counter['loop']}:
        """

        after = f"""
add $t7, $t7, $t9
sw $t7, {loop_variable}
j loop_{self.var_counter['loop']}
{end_loop}:
"""

        self.var_counter['loop'] += 1

        return before, [after]

    def to_mips(self, python_code):
        tokens = tokenize(python_code)
        ins_type = match_pattern(tokens)

        if ins_type == "PRINT":
            # handle negative numbers
            if len(tokens) == 3:
                arg = f"'-{tokens[-1]}'"
            else:
                arg = tokens[1]

            if isinstance(arg, int):
                return self.print_int(arg)
            elif isinstance(arg, str):
                argument_value = self.data_segment.get(arg)
                if isinstance(argument_value, int):
                    return self.print_var_int(arg)
                elif isinstance(argument_value, str):
                    return self.print_var_str(arg)
                elif argument_value == None:
                    var = f"str_literal_{self.var_counter['str']}"

                    self.assign([arg], var)
                    self.var_counter['str'] += 1
                    return self.print_var_str(var)

        elif ins_type == "ASSIGN":
            variable = tokens[0]
            args = tokens[2:]
            return self.assign(args, variable)

        elif ins_type == "CONDITIONAL":
            # before - a single mips line that should precede a block
            # after - list of mips lines that should follow a block
            before = after = ""

            if tokens[0] == 'else':
                last_marker = self.markers_stack.pop()
                last_marker.value = last_marker.alt_value
                after = f"{last_marker.label}:"
                return before, [after]

            op1, comp, op2 = tokens[1:]
            # OPPOSITE !!!
            ops = {"==": "bne", "<": "bge", ">": "ble",
                   "<=": "bgt", ">=": "blt", "!=": "beq"}

            if isinstance(op1, int) and isinstance(op2, int):
                if not eval("".join(map(str, tokens[1:]))):
                    end_label = f"label_{self.var_counter['label']}"
                    else_label = f"else_label_{self.var_counter['label']}"

                    self.var_counter["label"] += 1
                    before = f"j {end_label}"

                    if tokens[0] == "if":
                        marker = TemporaryMarker(f"{end_label}:\n",
                                                 f"j {else_label}\n{end_label}:\n",
                                                 else_label)
                        self.markers_stack.append(marker)

                    # marker can be activated or not depending on the
                    # existence of else in future line
                    after = [self.markers_stack[-1], f"{end_label}:\n"]

            else:
                compare_and_jump = self.__getattribute__(ops.get(comp))

                end_label = f"label_{self.var_counter['label']}"
                else_label = f"else_label_{self.var_counter['label']}"
                self.var_counter["label"] += 1

                if tokens[0] == "if":
                    marker = TemporaryMarker("",
                                             f"j {else_label}\n",
                                             else_label)
                    self.markers_stack.append(marker)

                before = compare_and_jump(op1, op2, end_label)

                # marker can be activated or not depending on the
                # existence of else in future line
                after = [self.markers_stack[-1], f"{end_label}:\n"]

            return (before, after)

        elif ins_type == "WHILE":
            op1, comp, op2 = tokens[1:]
            # OPPOSITE !!!
            ops = {"==": "bne", "<": "bge", ">": "ble",
                   "<=": "bgt", ">=": "blt", "!=": "beq"}

            if isinstance(op1, int) and isinstance(op2, int):
                if not eval("".join(map(str, tokens[1:]))):
                    end_label = f"loop_{self.var_counter['label']}"

                    self.var_counter["loop"] += 1
                    before = f"j {end_label}"

            else:
                compare_and_jump = self.__getattribute__(ops.get(comp))

                start_label = f"loop_{self.var_counter['loop']}"
                end_label = f"endloop_{self.var_counter['loop']}"
                self.var_counter["loop"] += 1

                before = f"{start_label}:\n" + \
                    compare_and_jump(op1, op2, end_label)

                after = [f"j {start_label}\n{end_label}:\n"]

            return (before, after)

        elif ins_type == "FOR":
            loop_variable = tokens[1]

            length = len(tokens[4:])

            if length == 1:
                start = 0
                end = tokens[4]
                step = 1
            elif length == 2:
                start = tokens[4]
                end = tokens[5]
                step = 1
            elif length == 3:
                start = tokens[4]
                end = tokens[5]
                step = tokens[6]
            elif length == 4:
                start = tokens[4]
                end = tokens[5]
                step = int("".join(tokens[6:]))

            return self.for_loop(start, end, step, loop_variable)

        return ""

    # def compile(self):
    #     for child in self.walk():
    #         yield self.to_mips(child)
    def compile(self):
        after = before = "#"
        for child in self.child:
            if isinstance(child, str):
                token = tokenize(child)
                ins_type = match_pattern(token)

                if ins_type in ("CONDITIONAL", "WHILE", "FOR"):
                    before, after = self.to_mips(child)
                    yield before

                else:
                    yield self.to_mips(child)

            else:
                yield from child.compile()
                for item in after:
                    yield item

    def walk(self):
        for child in self.child:
            if isinstance(child, str):
                yield child
            else:
                yield from child.walk()


class Compiler:
    def __init__(self, python_code):
        self.python_code = python_code
        self.data_segment = {}
        self.var_counter = {"str": 0, "label": 0, "loop": 0}
        self.markers_stack = []

    def get_root_block(self):
        blocks = [Block(self.data_segment, self.var_counter,
                        self.markers_stack)]

        self.python_code = self.python_code.replace("\t", "    ")

        prev = 0
        for line in self.python_code.split("\n"):
            if isblank(line):
                continue
            cur = blocks[-1]
            i = indent(line)
            if i == prev:
                cur.child.append(line.strip())

            elif i > prev:
                new = Block(self.data_segment, self.var_counter,
                            self.markers_stack)
                new.child.append(line.strip())
                cur.child.append(new)
                blocks.append(new)
            else:
                for _ in range((prev - i) // 4):
                    blocks.pop()
                cur = blocks[-1]

                cur.child.append(line.strip())
            prev = i

        return blocks[0]

    def build_data_segment(self):
        dataseg = [".data"]
        for varname, value in self.data_segment.items():
            if isinstance(value, int):
                dataseg.append(f"{varname}: .word {value}")

            elif isinstance(value, str):
                dataseg.append(f'{varname}: .asciiz "{value}"')

        return dataseg

    def compile(self):
        root_block = self.get_root_block()

        text_segment = [".text"]
        for mips in root_block.compile():
            text_segment.append(mips)

        data_segment = self.build_data_segment()

        mips_code = []
        mips_code.extend(text_segment)
        mips_code.extend(data_segment)

        return "\n".join(map(str, mips_code))


if __name__ == "__main__":
    with open("sample/print.py") as f:
        compiler = Compiler(f.read())
        mips = compiler.compile()
        print(mips)
