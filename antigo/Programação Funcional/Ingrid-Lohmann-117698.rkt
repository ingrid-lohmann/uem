#lang racket

(require examples)

;; Discente: Ingrid Lohmann RA: 117698

;; Tipos de dados

;; Velocidade medida é um número positivo com duas casas decimais;
;; Velocidade máxima é um número positivo com duas casas decimais;
;; Velocidade considerada é um número positivo com duas casas decimais;

;; Classidficação da multa
;;  - "leve"
;;  - "média"
;;  - "grave"
;;  - "gravíssima"

;; Classidficação da pontos 
;;  - "leve" -> 3 pontos
;;  - "média" -> 4 pontos
;;  - "grave" -> 5 pontos
;;  - "gravíssima" -> 7 pontos

;; Máximo de pontos é um número positivo sem casas decimais;



;; Questão 1

;;Velocidade-Máxima Velocidade-Medida -> Velocidade a ser considerada (Number)

;; Calcula a velocidade a ser considerada tendo como base a velocidade máxima do trecho, a ;; ;; velocidade base (107 Km/h) e a velocidade medida pelo radar do veículo, seguindo a lógica:
;;  - Se a velocidade medida do veículo <= 107 Km/h -> velocidade medida - 7 Km/h
;;  - Se a velocidade medida do veículo > 107 Km/h -> velocidade medida - 7% 

(examples
  (check-equal? (velocidade-considerada 80) 73)
  (check-equal? (velocidade-considerada 120) 111)
  (check-equal? (velocidade-considerada 106) 99)
  (check-equal? (velocidade-considerada 150) 139)
)

(define (velocidade-considerada velocidade-medida)
  (cond
    [(<= velocidade-medida 107) (exact-floor (- velocidade-medida 7))]
    [else
     (exact-floor (- velocidade-medida (* velocidade-medida 0.07)))
    ]
  )
)

;; Questão 2

;; Velocidade-Máxima Velocidade-Considerada -> Classificação da multa (String)

;; Calcula a classificação da multa tendo como base a velocidade máxima permitida no trecho e a ;; velocidade considerada no radar, seguindo a lógica:
;;  - Não existe infração leve para esse caso;
;;  - Se a velocidade considerada for > velocidade máxima + (1% < x < 20%) -> média
;;  - Se a velocidade considerada for > velocidade máxima + (20% <= x < 50%) -> grave
;;  - Se a velocidade considerada for > velocidade máxima + (x >= 50%) -> gravíssima

;; Exemplos
(examples
  (check-equal? (classifica-multa 60 50) "leve")
  (check-equal? (classifica-multa 100 106) "leve")
  (check-equal? (classifica-multa 100 120) "média")
  (check-equal? (classifica-multa 90 106.2) "média")
  (check-equal? (classifica-multa 80 113.6) "grave")
  (check-equal? (classifica-multa 60 87) "grave")
  (check-equal? (classifica-multa 60 150) "gravíssima")
  (check-equal? (classifica-multa 100 190) "gravíssima")
)


;; Exemplos porcentagem-velocidade-excedida
(examples
  (check-equal? (porcentagem-velocidade-excedida 100 106) -1)
  (check-equal? (porcentagem-velocidade-excedida 90 120) 23)
  (check-equal? (porcentagem-velocidade-excedida 80 113.6) 31)
  (check-equal? (porcentagem-velocidade-excedida 60 87) 33)
  (check-equal? (porcentagem-velocidade-excedida 60 150) 131)
  (check-equal? (porcentagem-velocidade-excedida 100 190) 76)
)

(define (porcentagem-velocidade-excedida  velocidade-maxima velocidade-medida)
  (exact-floor (- (/ (* (velocidade-considerada velocidade-medida) 100) velocidade-maxima) 100))
)


;; Exemplos esta-no-intervalo?
(examples
  (check-equal? (esta-no-intervalo? 1 20 16) #t)
  (check-equal? (esta-no-intervalo? 1 20 30) #f)
  (check-equal? (esta-no-intervalo? 20 50 49) #t)
  (check-equal? (esta-no-intervalo? 20 50 51) #f)
  (check-equal? (esta-no-intervalo? 50 100 130) #f)
)

(define (esta-no-intervalo? valor-minimo valor-maximo valor-calculado)
  (cond
    [(> valor-calculado 100) #f]
    [else
     (or
   (<= valor-calculado valor-minimo)
   (< valor-calculado valor-maximo)
  )
     ]
  )
)

;; Função final
(define (classifica-multa velocidade-maxima velocidade-medida)
  (define porcentagem (porcentagem-velocidade-excedida  velocidade-maxima velocidade-medida))
  (cond
   [(esta-no-intervalo? 0 1 porcentagem) "leve"]
   [(esta-no-intervalo? 1 20 porcentagem) "média"]
   [(esta-no-intervalo? 20 50 porcentagem) "grave"]
   [(esta-no-intervalo? 50 100 porcentagem) "gravíssima"]
   [else "gravíssima"]
  )
)


;; Questão 3

;; Obs: Professor, lendo o requisito achei que a escrita desse trecho estava errada, por conta disso  acabei fazendo a interpretação
;; do trecho abaixo do modo apresentado.

;; Quantidade de multas gravíssimas Quantidade de multas graves Quantidade de multas médias Quantidade de multas leves -> CNH Suspensa (boolean)

;; Calcula a quantidade de pontos necessários para o motorista ter a CNH suspensa recebendo a quantidade de cada um dos tipos de multas realizadas pelo motorista, seguindo a lógica:
;;  - Máximo de 40 pontos para motoristas que cometeram apenas multas classificadas como leve ou média (3 e 4 pontos para leve e média, respectivamente);
;;  - Máximo de 30 pontos para motoristas que cometeram multas classificadas como grave ou gravíssima (5 e 7 pontos para grave e gravíssima, respectivamente);
;;  - Máximo de 20 pontos para motoristas que cometeram apenas multas classificadas como grave (7 pontos por multa);


;; Exemplos
(examples
  (check-equal? (cnh-suspensa? 1 0 0 0) #f)
  (check-equal? (cnh-suspensa? 10 0 0 0) #t)
  (check-equal? (cnh-suspensa? 1 1 0 0) #f)
  (check-equal? (cnh-suspensa? 1 20 0 0) #t)
  (check-equal? (cnh-suspensa? 0 1 1 1) #f)
  (check-equal? (cnh-suspensa? 0 0 10 5) #t)
  (check-equal? (cnh-suspensa? 0 0 0 1) #f)
  (check-equal? (cnh-suspensa? 0 0 0 20) #t)
)


;; Exemplos calcula-pontos
(examples
  (check-equal? (calcula-pontos 3 3) 9)
  (check-equal? (calcula-pontos 34 7) 238)
  (check-equal? (calcula-pontos 7 7) 49)
  (check-equal? (calcula-pontos 2 5) 10)
)

(define (calcula-pontos quantidade pontos)
  (* quantidade pontos)
)


;; Exemplos calcula-pontos-total
(examples
  (check-equal? (calcula-pontos-total 1 0 1 1) 14)
  (check-equal? (calcula-pontos-total 0 1 1 1) 12)
  (check-equal? (calcula-pontos-total 0 0 1 1) 7)
  (check-equal? (calcula-pontos-total 0 0 0 1) 3)
  (check-equal? (calcula-pontos-total 1 0 0 1) 10)
)

(define (calcula-pontos-total qntd-gravissima qntd-grave qntd-media qntd-leve)
  (define total-gravissima (calcula-pontos qntd-gravissima 7))
  (define total-grave (calcula-pontos qntd-grave 5))
  (define total-media (calcula-pontos qntd-media 4))
  (define total-leve (calcula-pontos qntd-leve 3))
  (+ total-gravissima total-grave total-media total-leve)
)


;; Função final
(define (cnh-suspensa? qntd-gravissima qntd-grave qntd-media qntd-leve)
  (define pontos-total (calcula-pontos-total qntd-gravissima qntd-grave qntd-media qntd-leve))
  (cond
   [
    (and (and (> qntd-gravissima 0) (= qntd-grave 0)) (and (= qntd-media 0) (= qntd-leve 0)))
    (if (>= pontos-total 20) #t #f)
   ]
   [
    (or (> qntd-gravissima 0) (>  qntd-grave 0))
    (if (>= pontos-total 30) #t #f)
   ]
   [
    (or (> qntd-media 0) (> qntd-leve 0))
    (if (>= pontos-total 40) #t #f)
   ]
  )
)