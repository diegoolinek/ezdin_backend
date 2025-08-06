from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    # Remover todas as lições existentes
    Lesson.query.delete()
    db.session.commit()
    
    # Criar as tabelas se não existirem
    db.create_all()
    
    # Criar 10 lições de múltipla escolha
    lessons = [
        {
            "title": "Introdução à Educação Financeira",
            "content": "Bem-vindo à trilha de educação financeira! Aqui você aprenderá os conceitos fundamentais para controlar suas finanças. A educação financeira é essencial para tomar decisões conscientes sobre dinheiro, planejar o futuro e alcançar objetivos.",
            "challenge_question": "O que é educação financeira?",
            "option_a": "Aprender a gastar mais dinheiro",
            "option_b": "Aprender a controlar e planejar o uso do dinheiro",
            "option_c": "Guardar todo o dinheiro em casa",
            "option_d": "Não usar dinheiro nunca",
            "correct_option": "b",
            "explanation": "Educação financeira é aprender a controlar e planejar o uso do dinheiro para alcançar objetivos e ter uma vida mais tranquila.",
            "points_awarded": 10,
            "order_index": 1
        },
        {
            "title": "Entendendo Receitas e Despesas",
            "content": "Entender a diferença entre receitas e despesas é fundamental para o controle financeiro. Receitas são valores que entram em sua conta (salário, vendas, aluguéis recebidos), enquanto despesas são valores que saem (contas, compras, gastos diversos). O equilíbrio entre estes dois elementos é essencial para manter a saúde financeira.",
            "challenge_question": "Qual a diferença entre receita e despesa?",
            "option_a": "Receita é dinheiro que sai, despesa é dinheiro que entra",
            "option_b": "Receita é dinheiro que entra, despesa é dinheiro que sai",
            "option_c": "São a mesma coisa",
            "option_d": "Receita é só salário, despesa é só comida",
            "correct_option": "b",
            "explanation": "Receita é todo dinheiro que entra (salário, vendas, etc.) e despesa é todo dinheiro que sai (contas, compras, etc.).",
            "points_awarded": 10,
            "order_index": 2
        },
        {
            "title": "Criando um Orçamento Mensal",
            "content": "Criar um orçamento mensal é o primeiro passo para organizar suas finanças. Um orçamento é um planejamento que lista todas as receitas e despesas esperadas para o mês. Isso ajuda a controlar gastos, identificar onde é possível economizar e planejar investimentos.",
            "challenge_question": "Qual o primeiro passo para criar um orçamento mensal?",
            "option_a": "Comprar um caderno caro",
            "option_b": "Listar todas as receitas e despesas",
            "option_c": "Parar de gastar completamente",
            "option_d": "Pedir dinheiro emprestado",
            "correct_option": "b",
            "explanation": "O primeiro passo é listar todas as receitas (dinheiro que entra) e despesas (dinheiro que sai) para ter uma visão clara da situação financeira.",
            "points_awarded": 10,
            "order_index": 3
        },
        {
            "title": "A Importância de Poupar",
            "content": "Poupar significa separar uma parte da renda para o futuro. É importante criar o hábito de guardar dinheiro regularmente, mesmo que seja um valor pequeno. A regra 50-30-20 pode ajudar: 50% para necessidades básicas, 30% para desejos e lazer, 20% para poupança e investimentos.",
            "challenge_question": "Segundo a regra 50-30-20, qual porcentagem da renda deveria ser destinada à poupança?",
            "option_a": "10%",
            "option_b": "15%",
            "option_c": "20%",
            "option_d": "30%",
            "correct_option": "c",
            "explanation": "Na regra 50-30-20, recomenda-se destinar 20% da renda para poupança e investimentos.",
            "points_awarded": 10,
            "order_index": 4
        },
        {
            "title": "Conceitos Básicos de Investimento",
            "content": "Investir é fazer o dinheiro crescer ao longo do tempo. Existem diferentes tipos de investimentos: poupança (baixo risco e baixo retorno), CDB, Tesouro Direto, fundos de investimento e ações. É importante entender a relação risco x retorno: investimentos mais seguros geralmente rendem menos.",
            "challenge_question": "Qual investimento é considerado mais seguro e de baixo risco?",
            "option_a": "Ações na bolsa de valores",
            "option_b": "Poupança",
            "option_c": "Criptomoedas",
            "option_d": "Fundos imobiliários",
            "correct_option": "b",
            "explanation": "A poupança é considerada o investimento mais seguro, pois tem garantia do governo e baixo risco, mas também oferece retornos menores.",
            "points_awarded": 10,
            "order_index": 5
        },
        {
            "title": "Tipos de Despesas: Fixas e Variáveis",
            "content": "As despesas podem ser classificadas em dois tipos principais: fixas e variáveis. Despesas fixas são aquelas que se repetem todo mês com o mesmo valor (aluguel, financiamentos, seguros). Despesas variáveis mudam de valor mensalmente (alimentação, lazer, combustível). Conhecer essa diferença ajuda no planejamento.",
            "challenge_question": "Qual é um exemplo de despesa fixa?",
            "option_a": "Alimentação no restaurante",
            "option_b": "Aluguel da casa",
            "option_c": "Passeios no fim de semana",
            "option_d": "Compras de roupas",
            "correct_option": "b",
            "explanation": "O aluguel é uma despesa fixa porque tem o mesmo valor todos os meses e é obrigatória.",
            "points_awarded": 10,
            "order_index": 6
        },
        {
            "title": "Reserva de Emergência",
            "content": "A reserva de emergência é um valor guardado para situações imprevistas como perda de emprego, problemas de saúde ou emergências familiares. Recomenda-se ter entre 3 a 6 meses de gastos essenciais guardados em investimentos de alta liquidez (que podem ser resgatados rapidamente).",
            "challenge_question": "Quantos meses de gastos essenciais devem compor uma reserva de emergência?",
            "option_a": "1 mês",
            "option_b": "2 meses",
            "option_c": "3 a 6 meses",
            "option_d": "12 meses",
            "correct_option": "c",
            "explanation": "A reserva de emergência ideal deve cobrir entre 3 a 6 meses de gastos essenciais para dar segurança em situações imprevistas.",
            "points_awarded": 10,
            "order_index": 7
        },
        {
            "title": "Cartão de Crédito: Uso Consciente",
            "content": "O cartão de crédito é uma ferramenta financeira útil quando usado com responsabilidade. Permite parcelar compras e oferece prazo para pagamento, mas cobra juros altos se não for pago integralmente. O ideal é usar apenas o que consegue pagar e sempre quitar a fatura completa.",
            "challenge_question": "Qual a melhor prática no uso do cartão de crédito?",
            "option_a": "Usar o limite máximo sempre",
            "option_b": "Pagar apenas o valor mínimo",
            "option_c": "Quitar a fatura completa todo mês",
            "option_d": "Usar para investimentos",
            "correct_option": "c",
            "explanation": "A melhor prática é quitar a fatura completa todos os meses para evitar juros altos e manter a saúde financeira.",
            "points_awarded": 10,
            "order_index": 8
        },
        {
            "title": "Consumo Consciente",
            "content": "Consumo consciente significa distinguir entre necessidades e desejos antes de comprar. Necessidades são gastos essenciais (moradia, alimentação, saúde), enquanto desejos são itens que gostaríamos de ter mas não são indispensáveis. Planejar compras e comparar preços ajuda a economizar.",
            "challenge_question": "Qual é a principal diferença entre necessidade e desejo?",
            "option_a": "Necessidade é cara, desejo é barato",
            "option_b": "Necessidade é essencial para viver, desejo é supérfluo",
            "option_c": "São a mesma coisa",
            "option_d": "Desejo é mais importante que necessidade",
            "correct_option": "b",
            "explanation": "Necessidade é algo essencial para viver (como alimentação e moradia), enquanto desejo é algo que gostaríamos de ter mas não é indispensável.",
            "points_awarded": 10,
            "order_index": 9
        },
        {
            "title": "Planejamento de Objetivos Financeiros",
            "content": "Ter objetivos financeiros claros é fundamental para o sucesso das finanças pessoais. Podem ser objetivos de curto prazo (até 1 ano), médio prazo (1 a 5 anos) ou longo prazo (mais de 5 anos). Cada objetivo deve ter valor definido, prazo estabelecido e estratégia de como alcançá-lo através de poupança e investimentos adequados.",
            "challenge_question": "Como são classificados os objetivos financeiros quanto ao tempo?",
            "option_a": "Pequenos, médios e grandes",
            "option_b": "Curto, médio e longo prazo",
            "option_c": "Fáceis e difíceis",
            "option_d": "Pessoais e profissionais",
            "correct_option": "b",
            "explanation": "Os objetivos financeiros são classificados em curto prazo (até 1 ano), médio prazo (1 a 5 anos) e longo prazo (mais de 5 anos).",
            "points_awarded": 10,
            "order_index": 10
        }
    ]
    
    for lesson_data in lessons:
        lesson = Lesson(**lesson_data)
        db.session.add(lesson)
    
    db.session.commit()
    print(f"Criadas {len(lessons)} lições de múltipla escolha!")
    print("Lições criadas:")
    for lesson_data in lessons:
        print(f"- {lesson_data['order_index']}: {lesson_data['title']}")
