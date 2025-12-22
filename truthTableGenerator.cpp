#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stack>
#include <algorithm>
#include <cctype> 

// Enum para representar os tipos de token
enum TokenType {
    VARIABLE,
    OPERATOR,
    PARENTHESIS
};

// Estrutura para um token
struct Token {
    std::string value;
    TokenType type;
};

// Função para verificar se um caractere é parte de um nome de variável
bool isVariableChar(char c) {
    return isalnum(c) || c == '_';
}

// Tokeniza a string de expressão
std::vector<Token> tokenize(const std::string& expression) {
    std::vector<Token> tokens;
    for (size_t i = 0; i < expression.length(); ) {
        char c = expression[i];
        if (isspace(c)) {
            i++;
            continue;
        }

        if (c == '+' || c == '*' || c == '!') {
            tokens.push_back({std::string(1, c), OPERATOR});
            i++;
        } else if (c == '(' || c == ')') {
            tokens.push_back({std::string(1, c), PARENTHESIS});
            i++;
        } else if (isalpha(c) || c == '_') {
            std::string varName = "";
            while (i < expression.length() && isVariableChar(expression[i])) {
                varName += expression[i];
                i++;
            }
            tokens.push_back({varName, VARIABLE});
        } else {
            // Caractere desconhecido, você pode adicionar um tratamento de erro aqui
            std::cerr << "Erro: Caractere invalido na expressao: " << c << std::endl;
            return {}; // Retorna vetor vazio em caso de erro
        }
    }
    return tokens;
}

// Precedência dos operadores
int precedence(const std::string& op) {
    if (op == "!") return 3;
    if (op == "*") return 2;
    if (op == "+") return 1;
    return 0;
}

// Converte a lista de tokens para notação pós-fixa (RPN)
std::vector<Token> infixToPostfix(const std::vector<Token>& infixTokens) {
    std::vector<Token> postfixTokens;
    std::stack<Token> opStack;

    for (const auto& token : infixTokens) {
        if (token.type == VARIABLE) {
            postfixTokens.push_back(token);
        } else if (token.value == "(") {
            opStack.push(token);
        } else if (token.value == ")") {
            while (!opStack.empty() && opStack.top().value != "(") {
                postfixTokens.push_back(opStack.top());
                opStack.pop();
            }
            if (!opStack.empty()) opStack.pop(); // Remove o '('
        } else if (token.type == OPERATOR) {
            while (!opStack.empty() && opStack.top().type == OPERATOR && precedence(opStack.top().value) >= precedence(token.value)) {
                postfixTokens.push_back(opStack.top());
                opStack.pop();
            }
            opStack.push(token);
        }
    }

    while (!opStack.empty()) {
        postfixTokens.push_back(opStack.top());
        opStack.pop();
    }
    return postfixTokens;
}

// Avalia a expressão em notação pós-fixa
bool evaluatePostfix(const std::vector<Token>& postfixTokens, const std::map<std::string, bool>& values) {
    std::stack<bool> operandStack;

    for (const auto& token : postfixTokens) {
        if (token.type == VARIABLE) {
            if (values.count(token.value)) {
                operandStack.push(values.at(token.value));
            } else {
                std::cerr << "Erro: Variavel nao encontrada: " << token.value << std::endl;
                return false;
            }
        } else if (token.value == "!") {
            if (operandStack.empty()) { std::cerr << "Erro de expressao (NOT). " << std::endl; return false; }
            bool val = operandStack.top();
            operandStack.pop();
            operandStack.push(!val);
        } else if (token.value == "*" || token.value == "+") {
            if (operandStack.size() < 2) { std::cerr << "Erro de expressao (" << token.value << "). " << std::endl; return false; }
            bool right = operandStack.top();
            operandStack.pop();
            bool left = operandStack.top();
            operandStack.pop();

            if (token.value == "*") { // AND
                operandStack.push(left && right);
            } else { // OR
                operandStack.push(left || right);
            }
        }
    }

    if (operandStack.size() != 1) { std::cerr << "Erro de expressao final. " << std::endl; return false; }
    return operandStack.top();
}

int main() {
    std::string expression = "";
    std::cout << "Digite a expressao booleana (use +, *, !, ( e ) e nomes de variaveis com letras, numeros e _): ";
    std::getline(std::cin, expression);

    // Etapa 1: Tokenização
    std::vector<Token> infixTokens = tokenize(expression);
    if (infixTokens.empty()) return 1;

    // Etapa 2: Encontrar as variáveis
    std::vector<std::string> variables;
    for (const auto& token : infixTokens) {
        if (token.type == VARIABLE) {
            bool found = false;
            for(const auto& var : variables) {
                if(var == token.value) {
                    found = true;
                    break;
                }
            }
            if(!found) {
                variables.push_back(token.value);
            }
        }
    }
    std::sort(variables.begin(), variables.end());

    // Etapa 3: Converter para notação pós-fixa
    std::vector<Token> postfixTokens = infixToPostfix(infixTokens);

    // Etapa 4: Imprimir o cabeçalho
    for (const auto& var : variables) {
        std::cout << var << "\t";
    }
    std::cout << "| Resultado\n";
    std::cout << "--------------------------------\n";

    // Etapa 5: Gerar e avaliar todas as combinações
    int numVariables = variables.size();
    if (numVariables > 20) {
        std::cerr << "Aviso: Mais de 20 variaveis, a tabela verdade sera muito grande (" << (1 << numVariables) << " linhas) e pode demorar muito." << std::endl;
    }

    int numCombinations = 1 << numVariables;

    for (int i = 0; i < numCombinations; ++i) {
        std::map<std::string, bool> variableValues;
        for (int j = 0; j < numVariables; ++j) {
            bool value = (i >> j) & 1;
            variableValues[variables[j]] = value;
            std::cout << (value ? "V" : "F") << "\t";
        }

        bool result = evaluatePostfix(postfixTokens, variableValues);
        std::cout << "| " << (result ? "V" : "F") << "\n";
    }

    return 0;
}