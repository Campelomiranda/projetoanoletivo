/**
 * CityLens Sorocaba — cria automaticamente o Google Forms da pesquisa de campo.
 *
 * COMO USAR (2 min):
 *  1. Acesse https://script.google.com  →  "Novo projeto".
 *  2. Apague o conteúdo e cole TODO este arquivo.
 *  3. Menu "Executar" (▶) na função criarFormularioCityLens.
 *     Na 1ª vez o Google pede autorização — permita (é seu próprio Drive).
 *  4. Veja o link do formulário impresso em "Execução" (Ctrl+Enter mostra o log).
 *     O formulário e a planilha de respostas ficam salvos no seu Google Drive.
 *
 * Regra do projeto: são PERCEPÇÕES e distâncias autodeclaradas (não medições
 * oficiais). Para separar bem as regiões, colete um número parecido de respostas
 * por zona (meta: pelo menos 10 por zona).
 */
function criarFormularioCityLens() {
  var form = FormApp.create('CityLens Sorocaba — Pesquisa de campo (acesso urbano por região)');
  form.setDescription(
    'Ajude a mapear o acesso a serviços e a acessibilidade nas regiões de Sorocaba. ' +
    'São ~5 minutos. Responda pensando na SUA região (onde mora ou passa a maior parte do tempo). ' +
    'Não há resposta certa — queremos a sua percepção real. Respostas anônimas.'
  );
  form.setProgressBar(true);
  form.setCollectEmail(false);

  var ZONAS = ['Centro', 'Zona Norte', 'Zona Oeste', 'Zona Sul', 'Zona Leste', 'Zona Industrial', 'Não sei / outra'];
  var TEMPO = ['Menos de 5 min', '5 a 10 min', '10 a 20 min', 'Mais de 20 min', 'Não dá para ir a pé', 'Não sei'];
  var LIKERT_RUIM_BOM = ['Muito ruim', 'Ruim', 'Regular', 'Bom', 'Muito bom'];

  // ----- Seção 1: sua região -----
  form.addSectionHeaderItem().setTitle('1. Sua região').setHelpText('Para agrupar as respostas por zona.');
  form.addListItem().setTitle('Em qual ZONA de Sorocaba você mora (ou passa a maior parte do tempo)?')
      .setChoiceValues(ZONAS).setRequired(true);
  form.addTextItem().setTitle('Qual o seu BAIRRO?')
      .setHelpText('Escreva o nome do bairro (ajuda a conferir a zona).');
  form.addMultipleChoiceItem().setTitle('Há quanto tempo você conhece bem essa região?')
      .setChoiceValues(['Menos de 1 ano', '1 a 5 anos', 'Mais de 5 anos'])
      .showOtherOption(false);

  // ----- Seção 2: distância/tempo a pé (discrimina bem as zonas) -----
  form.addPageBreakItem().setTitle('2. Quanto tempo a pé até…')
      .setHelpText('Da sua casa, andando, até o mais próximo de cada tipo. Se não usa, chute o mais perto que conhece.');
  [['o ponto de ônibus mais próximo?'],
   ['a UBS / posto de saúde mais próximo?'],
   ['a escola mais próxima?'],
   ['o mercado ou a farmácia mais próximos?'],
   ['a praça ou o parque mais próximos?']
  ].forEach(function (q) {
    form.addMultipleChoiceItem().setTitle('Tempo a pé até ' + q[0]).setChoiceValues(TEMPO).setRequired(true);
  });
  form.addMultipleChoiceItem().setTitle('Com que frequência passam ônibus na sua região?')
      .setChoiceValues(['Vários por hora', '± 1 por hora', 'Poucos por dia', 'Quase nenhum', 'Não sei']);

  // ----- Seção 3: acessibilidade da caminhada (tema do projeto, sem dado objetivo hoje) -----
  form.addPageBreakItem().setTitle('3. Andar a pé e acessibilidade')
      .setHelpText('Pensando em quem anda a pé, idosos, cadeirantes ou com carrinho de bebê.');
  form.addScaleItem().setTitle('Como são as CALÇADAS da sua região?')
      .setBounds(1, 5).setLabels('Muito ruins', 'Muito boas').setRequired(true);
  form.addMultipleChoiceItem().setTitle('As esquinas têm RAMPAS de acessibilidade?')
      .setChoiceValues(['Sim, na maioria', 'Em algumas', 'Quase nenhuma', 'Nenhuma', 'Não sei']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('Existe PISO TÁTIL (piso para pessoas cegas) nas calçadas?')
      .setChoiceValues(['Sim, em vários pontos', 'Em poucos pontos', 'Não existe', 'Não sei']);
  form.addMultipleChoiceItem().setTitle('Há semáforos com SINAL SONORO para pessoas cegas?')
      .setChoiceValues(['Sim', 'Não', 'Não sei']);
  form.addScaleItem().setTitle('Facilidade para andar com CADEIRA DE RODAS ou carrinho de bebê')
      .setBounds(1, 5).setLabels('Muito difícil', 'Muito fácil');
  form.addScaleItem().setTitle('ILUMINAÇÃO das ruas à noite')
      .setBounds(1, 5).setLabels('Muito ruim', 'Muito boa');

  // ----- Seção 4: percepção geral (grade Likert, mesma escala p/ todos os eixos) -----
  form.addPageBreakItem().setTitle('4. No geral, como você avalia o acesso a…');
  form.addGridItem().setTitle('Na sua região, o acesso a cada item é:')
      .setRows(['Saúde (postos/UBS)', 'Escolas', 'Comércio e serviços', 'Ônibus / transporte',
                'Praças e áreas verdes', 'Segurança'])
      .setColumns(LIKERT_RUIM_BOM).setRequired(true);

  // ----- Seção 5: prioridades e perfil -----
  form.addPageBreakItem().setTitle('5. Para terminar');
  form.addCheckboxItem().setTitle('O que MAIS falta na sua região? (marque até 3)')
      .setChoiceValues(['Saúde', 'Escolas', 'Transporte / ônibus', 'Comércio', 'Praças e áreas verdes',
                        'Calçadas e acessibilidade', 'Iluminação', 'Segurança', 'Limpeza']);
  form.addMultipleChoiceItem().setTitle('Você ou alguém da sua casa tem deficiência ou mobilidade reduzida?')
      .setChoiceValues(['Sim', 'Não', 'Prefiro não dizer']);
  form.addMultipleChoiceItem().setTitle('Sua faixa etária')
      .setChoiceValues(['Até 17', '18 a 29', '30 a 45', '46 a 59', '60 ou mais']);
  form.addParagraphTextItem().setTitle('Algo a acrescentar sobre a sua região? (opcional)');

  // planilha de respostas
  var ss = SpreadsheetApp.create('CityLens — respostas da pesquisa de campo');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('FORMULÁRIO (para responder): ' + form.getPublishedUrl());
  Logger.log('EDITAR o formulário: ' + form.getEditUrl());
  Logger.log('PLANILHA de respostas: ' + ss.getUrl());
}
