# maquina_norma_completa.py
# Arquivo Único: Contém a definição da Máquina Norma e a interface para execução.

import time
import os

# --------------------------------------------------------------------------
# PARTE 1: DEFINIÇÃO DA CLASSE DA MÁQUINA NORMA
# (Anteriormente no arquivo norma_machine.py)
# --------------------------------------------------------------------------

class NormaMachine:
    """
    Simulador para a Máquina Norma conforme especificado.
    """
    def __init__(self):
        """
        Inicializa a máquina com 8 registradores zerados.
        """
        self.registers = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
        self.program = {}
        self.pc = 0  # Program Counter
        self.start_line = 0

    def set_registers(self, initial_values):
        """
        Permite ao usuário inicializar os registradores com valores determinados.
        Por exemplo: {'A': 5, 'B': 4}
        """
        # Zera todos os registradores antes de definir novos valores
        for reg in self.registers:
            self.registers[reg] = 0
            
        for reg, value in initial_values.items():
            if reg.upper() in self.registers:
                try:
                    self.registers[reg.upper()] = int(value)
                except ValueError:
                    print(f"Aviso: Valor inválido para o registrador {reg.upper()}. Usando 0.")
                    self.registers[reg.upper()] = 0
            else:
                print(f"Aviso: Registrador desconhecido '{reg}'. Ignorando.")

    def _parse_line(self, line: str):
        """
        Analisa uma linha do programa no formato "rótulo: OP REG JUMP(s)".
        Ex: "3: ZER A 4 1"
        """
        try:
            label_part, instr_part = line.strip().split(':', 1)
            label = int(label_part)
            parts = instr_part.strip().split()
            
            op = parts[0].upper()
            reg = parts[1].upper()
            jumps = [int(j) for j in parts[2:]]

            if op not in ["ADD", "SUB", "ZER"]:
                raise ValueError(f"Operação desconhecida '{op}' na linha {label}.")
            if reg not in self.registers:
                raise ValueError(f"Registrador desconhecido '{reg}' na linha {label}.")
            if op in ["ADD", "SUB"] and len(jumps) != 1:
                raise ValueError(f"Instrução {op} na linha {label} deve ter 1 desvio.")
            if op == "ZER" and len(jumps) != 2:
                raise ValueError(f"Instrução {op} na linha {label} deve ter 2 desvios.")

            return label, {'op': op, 'reg': reg, 'jumps': jumps}
        except Exception as e:
            print(f"Erro ao analisar a linha: '{line.strip()}'. {e}")
            return None, None

    def load_program(self, filepath: str):
        """
        Lê um programa monolítico de um arquivo.
        """
        self.program = {}
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        label, instruction = self._parse_line(line)
                        if label is not None:
                            self.program[label] = instruction
            if not self.program:
                print("Aviso: Nenhum programa carregado. O arquivo pode estar vazio ou mal formatado.")
                return False
            self.start_line = min(self.program.keys())
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filepath}' não encontrado.")
            return False

    def _print_state(self, note=""):
        """
        Exibe o estado atual dos registradores e a próxima instrução.
        """
        regs_to_show = ('A', 'B', 'C', 'D', 'E')
        reg_values = tuple(self.registers[r] for r in regs_to_show)

        instruction_desc = ""
        pc_display = self.pc
        
        if note == "Entrada de Dados":
            instruction_desc = "M (Entrada de Dados)"
            pc_display = self.start_line
        elif note == "FIM":
            instruction_desc = f"HALT (Desvio para linha inexistente: {self.pc})"
            pc_display = "FIM"
        else:
            instr = self.program.get(self.pc)
            if instr:
                op, reg, jumps = instr['op'], instr['reg'], instr['jumps']
                if op == "ADD":
                    instruction_desc = f"FACA ADD ({reg}) VA_PARA {jumps[0]}"
                elif op == "SUB":
                    instruction_desc = f"FACA SUB ({reg}) VA_PARA {jumps[0]}"
                elif op == "ZER":
                    instruction_desc = f"SE ZER ({reg}) ENTAO VA_PARA {jumps[0]} SENAO VA_PARA {jumps[1]}"

        print(f"{str(reg_values):<18} | Linha: {str(pc_display):<5} | Instrução: {instruction_desc}")

    def run(self, verbose=True, delay=0.1):
        """
        Executa o programa carregado.
        """
        if not self.program:
            print("Nenhum programa para executar.")
            return

        self.pc = self.start_line
        
        print("-" * 70)
        self._print_state(note="Entrada de Dados")
        time.sleep(delay*2)

        while self.pc in self.program:
            if verbose:
                self._print_state()
                time.sleep(delay)

            instr = self.program[self.pc]
            op, reg, jumps = instr['op'], instr['reg'], instr['jumps']

            if op == 'ADD':
                self.registers[reg] += 1
                self.pc = jumps[0]
            elif op == 'SUB':
                if self.registers[reg] > 0:
                    self.registers[reg] -= 1
                self.pc = jumps[0]
            elif op == 'ZER':
                if self.registers[reg] == 0:
                    self.pc = jumps[0]
                else:
                    self.pc = jumps[1]
        
        print("-" * 70)
        self._print_state(note="FIM")
        print("\nExecução encerrada.")
        print("\nEstado final dos registradores:")
        print(self.registers)
        print("-" * 70)


# --------------------------------------------------------------------------
# PARTE 2: INTERFACE DO MENU E EXECUÇÃO
# (Anteriormente no arquivo main.py)
# --------------------------------------------------------------------------

def get_initial_values(registers_needed):
    """Solicita ao usuário os valores iniciais para os registradores."""
    values = {}
    print(f"\nPor favor, insira os valores iniciais.")
    for reg in registers_needed:
        while True:
            try:
                val = input(f"  > Valor para o registrador {reg}: ")
                values[reg] = int(val)
                break
            except ValueError:
                print("    ERRO: Por favor, insira um número inteiro.")
    return values

def main_menu():
    # A classe NormaMachine já está definida acima, então podemos usá-la diretamente.
    machine = NormaMachine()

    programs = {
        "1": {"file": "soma.txt", "regs": ['A', 'B']},
        "2": {"file": "multiplicacao.txt", "regs": ['A', 'B']},
        "3": {"file": "fatorial.txt", "regs": ['A']}
    }

    while True:
        print("\n--- Simulador de Máquina Norma ---")
        print("Escolha o programa para executar:")
        print("1: Soma (C := A + B)")
        print("2: Multiplicação (A := A * B)")
        print("3: Fatorial (B := Fatorial(A))")
        print("4: Sair")

        choice = input("> ")

        if choice == '4':
            print("Encerrando.")
            break
        
        if choice in programs:
            prog_info = programs[choice]
            prog_file = prog_info["file"]

            if not os.path.exists(prog_file):
                print(f"\nERRO FATAL: Arquivo de programa '{prog_file}' não encontrado.")
                print("Certifique-se de que ele está na mesma pasta que o script Python.")
                continue

            initial_regs = get_initial_values(prog_info["regs"])
            
            machine.set_registers(initial_regs)
            
            if machine.load_program(prog_file):
                print("\nIniciando a execução do programa...")
                machine.run()
        else:
            print("Opção inválida. Por favor, escolha de 1 a 4.")

# Ponto de entrada do programa: executa o menu principal
if __name__ == "__main__":
    main_menu()