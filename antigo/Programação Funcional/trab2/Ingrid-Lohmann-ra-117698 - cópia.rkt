#lang racket

(require examples)

;; Tipos de dados

;; Lista com o código do aluno, nota da redação e alternativas marcadas contendo números positivos;
;; Lista com o gabarito contendo números positivos;

;; Cálculo da nota da somatória

;; Cada questão vale 6 pontos, sendo que cada questão pode ter 0 a 5 alternativas certas. Sendo assim o valor de cada questão correta é dado por 6/(número de questões corretas).

;; O valor final da nota do candidato é dada pela soma das 5 questões mais a nota da redação, caso ela seja maior que 1. Se o candidato zerar a redação é desclassificado, mesmo que tenha gabaritado as questões.

;; FUNÇÕES AUXILIARES

;; Alternativa é um dos valores: 1, 2, 4, 8, 16.

;; Somatório é um número natural entre 0 e 31.
;; Somatório -> Lista(Alternativa)

;; Calcula a lista de alternativas que somadas gera o somátorio s.
(examples
(check-equal? (somatorio->alternativas 0) empty)
(check-equal? (somatorio->alternativas 1) (list 1))
(check-equal? (somatorio->alternativas 21) (list 1 4 16))
(check-equal? (somatorio->alternativas 10) (list 2 8))
(check-equal? (somatorio->alternativas 31) (list 1 2 4 8 16)))

(define (somatorio->alternativas s)
  
  ; Decompõe num com divisões sucessivas por 2.
  ; Se num é ímpar, o último dígito binário é 1, então a alternativa está presente.

  (define (iter num alternativa)
    (cond
      [(zero? num) empty]
      [(odd? num) ; último dígito binário é 1
        (cons alternativa (iter (quotient num 2) (* 2 alternativa)))]
      [else (iter (quotient num 2) (* 2 alternativa))])
  )
  (iter s 1)
)


;; Calcula o valor de cada alternativa dependendo da quatidade de alternativas corretas
;; Número -> Número decimal
(examples
  (check-equal? (valor-questao 0) 0)
  (check-equal? (valor-questao 1) 6.0)
  (check-equal? (valor-questao 3) 2.0)
  (check-equal? (valor-questao 2) 3.0)
  (check-equal? (valor-questao 5) 1.2)
)


(define (valor-questao quantidade-certas)
  (cond
    [(= quantidade-certas 0) 0]
    [else (exact->inexact(/ 6 quantidade-certas))]
  )
)


;; Soma os elementos de uma lista
;; Lista(Números) -> Número 
(examples
  (check-equal? (soma-elementos '(1 2 3)) 6)
  (check-equal? (soma-elementos '(1 1 1)) 3)
  (check-equal? (soma-elementos '(2)) 2)
)


(define (soma-elementos lst)
  (cond
    [(empty? lst) 0]
    [else
      (+ (first lst) (soma-elementos (rest lst)))
    ]
  )
)


;; Verifica se um determinado número está na lista. Retorna 1 para #t e 0 para #f
;; Lista(Números) -> Número (0 ou 1)
(examples
  (check-equal? (esta-na-lista '(1 2 3) 1) 1)
  (check-equal? (esta-na-lista '(1 1 1) 1) 1)
  (check-equal? (esta-na-lista '(2 3 4 5 6) 2) 1)
  (check-equal? (esta-na-lista '(2 3 4 5 6) 7) 0)
)

(define (esta-na-lista list value)
 (cond
    [(empty? list) 0]
    [(= (first list) value) (add1 0)]
    [else (esta-na-lista (rest list) value)]
  )
)


;;Confere a quantidade de alternativas corretas por questão
;; Lista(Números) -> Número 
(examples
  (check-equal? (confere-numero-corretas '(1 2 3) '(1 2 3)) 3)
  (check-equal? (confere-numero-corretas '(2 3 4 5 6) '(1 7 8 9)) 0)
  (check-equal? (confere-numero-corretas '(21 10 08 16 15) '(4 10 4 16 10)) 2)
)


(define (confere-numero-corretas gabarito resposta)
  (soma-elementos
    (map 
      (lambda (n) (esta-na-lista resposta n))
      gabarito)
  )
)


;; Calcula o valor obtido em cada questão
;; Número Número -> Número decimal
(examples
  (check-equal? (pontuacao-por-questao 23 16) 1.5)
  (check-equal? (pontuacao-por-questao 7 5) 4.0)
  (check-equal? (pontuacao-por-questao 0 0) 6.0)
  (check-equal? (pontuacao-por-questao 12 5) 3.0)
  (check-equal? (pontuacao-por-questao 18 2) 3.0)
)

(define (pontuacao-por-questao gabarito resposta)
  (cond
    [(and (= gabarito 0) (= resposta 0)) 6.0]
    [else
      (define lista-gabarito (somatorio->alternativas gabarito))
  
      (define lista-resposta (somatorio->alternativas resposta))

      (define tam-lista-gabarito (length lista-gabarito))
  
      (define valor (valor-questao tam-lista-gabarito))
  
      (define qnt-corretas (confere-numero-corretas lista-gabarito lista-resposta))

      (* valor qnt-corretas)
    ]
  )
)


;; Calcula o valor obtida com a soma das alternativas corretas
;; Lista(Número) Lista(Número) -> Número decimal
(examples
  (check-equal? (pontuacao-parcial-respostas '(23 7 0 12 18) '(16 5 0 5 2)) 17.5)
  (check-equal? (pontuacao-parcial-respostas '(23 10 8 16 15) '(4 10 4 16 10)) 16.5)
  (check-equal? (pontuacao-parcial-respostas '(23 7 31 12 18) '(10 4 8 15 9)) 10.7)
  (check-equal? (pontuacao-parcial-respostas '(10 15 3 7 0) '(10 15 3 7 0)) 30.0)
  (check-equal? (pontuacao-parcial-respostas '(10 15 3 7 0) '(0 16 4 8 2)) 0)
)


(define (pontuacao-parcial-respostas gabarito respostas)
  (soma-elementos
    (map 
      (lambda (number1 number2) (pontuacao-por-questao number1 number2))
      gabarito
      respostas
    )
  )
)


;;Calcula a pontuação final, somando a nota da redação com o valor obtido nas questões
;; Lista(Número) Lista(Número) Número -> Lista(Número)
(examples
  (check-equal? (pontuacao-final '(23 7 0 12 18) 333 '(16 5 0 5 2) 80) '(333 97.5))
  (check-equal? (pontuacao-final '(23 10 8 16 15) 231 '(4 10 4 16 10) 60) '(231 76.5))
  (check-equal? (pontuacao-final '(23 7 31 12 18) 987 '(10 4 8 15 9) 0) '(987 10.7))
  (check-equal? (pontuacao-final '(10 15 3 7 0) 444 '(10 15 3 7 0) 100) '(444 130.0))
  (check-equal? (pontuacao-final '(10 15 3 7 0) 678 '(0 16 4 8 2) 25) '(678 25))
)

(define (pontuacao-final gabarito cod-candidato respostas nota-redacao)
  (define pontuacao-respostas (pontuacao-parcial-respostas gabarito respostas))

  (define pontuacao (+ pontuacao-respostas nota-redacao))
  (list cod-candidato pontuacao)
)


;; Filtra a lista de candidatos, retornando apenas aqueles que não zeraram a redação
;; Lista(Lista(Números)) -> Lista 
(examples
  (check-equal? (filtra-classificados '((123 11 4 10 4 16 10) (111 0 5 6 6 7))) '((123 11 4 10 4 16 10)))
  (check-equal? (filtra-classificados '((123 11 4 10 4 16 10) (111 0 5 6 6 7) (333 40 5 6 7 7))) '((123 11 4 10 4 16 10) (333 40 5 6 7 7)))
  (check-equal? (filtra-classificados '((123 78 23 7 31 12 18))) '((123 78 23 7 31 12 18)))
  (check-equal? (filtra-classificados '((111 0 5 6 6 7))) '())
)

(define (filtra-classificados candidatos-lista)
  (filter-not empty? 
    (map 
        (lambda (lst1)
          (if (= (second lst1) 0) '() lst1)
        )
        candidatos-lista
    )
  )
)


;; FUNÇÃO FINAL

;; Recebe o gabarito(Lista) e a lista de candidatos com seus respectivos códigos, notas da redação e questões marcadas
;; Retorna uma lista com o código e nota de cada candidato aprovado.
;; Lista(Números) -> Lista(Lista (Números)) 
(examples
  (check-equal? (classificacao-final (list 21 10 8 16 15) '((123 11 (4 10 4 16 10)) (111 0 (1 2 3 4 5)) (333 40 (21 8 8 8 14)))) '((123 28.0) (333 59.5)))
  (check-equal? (classificacao-final (list 21 10 8 16 15) '((345 5 (23 7 31 12 18)))) '((345 21.5)))
  (check-equal? (classificacao-final (list 21 10 8 16 15) '((3211 80 (4 10 4 16 10)) (7102 0 (1 2 3 4 5)) (1234 90 (21 8 8 8 14)) (5812 32 (20 0 8 16 1)) (9123 0 (5 4 3 2 1)))) '((3211 97.0) (1234 109.5) (5812 49.5)))
)

(define (classificacao-final gabarito candidatos-lista)
  (define lista-final (filtra-classificados candidatos-lista))
  (map 
     (lambda (elemento) (pontuacao-final gabarito (first elemento) (third elemento) (second elemento)))
     lista-final
  )
)

;; Exemplo final para ser usado
;; (classificacao-final (list 21 10 8 16 15) '((123 11 (4 10 4 16 10)) (111 0 (1 2 3 4 5)) (333 40 (21 8 8 8 14))))
