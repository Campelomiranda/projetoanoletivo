/**
 * CityLens Sorocaba — cria o Google Forms da PESQUISA RÁPIDA (~2 min, 8 perguntas).
 * Uso: script.google.com → Novo projeto → cole tudo → Executar (▶). Autorize.
 * Os links (responder / editar / planilha) aparecem no log.
 * São percepções/autodeclarado, não medição oficial.
 */
function criarFormularioCityLens() {
  var form = FormApp.create('CityLens Sorocaba — pesquisa rápida (2 min)');
  form.setDescription('Responda pensando na SUA região (onde mora ou passa a maior parte do tempo). '
    + '~2 minutos, anônimo. Não há resposta certa — queremos a sua percepção.');
  form.setProgressBar(true);
  form.setCollectEmail(false);

  var ZONAS = ['Centro', 'Zona Norte', 'Zona Oeste', 'Zona Sul', 'Zona Leste', 'Zona Industrial', 'Não sei / outra'];
  var TEMPO = ['Menos de 5 min', '5 a 10 min', '10 a 20 min', 'Mais de 20 min', 'Não dá a pé', 'Não sei'];
  var ESCALA = ['Muito ruim', 'Ruim', 'Regular', 'Bom', 'Muito bom'];

  form.addListItem().setTitle('1) Qual a sua ZONA em Sorocaba?').setChoiceValues(ZONAS).setRequired(true);
  form.addTextItem().setTitle('2) Bairro (opcional)');
  form.addMultipleChoiceItem().setTitle('3) Tempo a pé até o ponto de ônibus mais próximo')
      .setChoiceValues(TEMPO).setRequired(true);
  form.addMultipleChoiceItem().setTitle('4) Tempo a pé até a UBS / posto de saúde mais próximo')
      .setChoiceValues(TEMPO).setRequired(true);
  form.addMultipleChoiceItem().setTitle('5) As esquinas têm rampas de acessibilidade?')
      .setChoiceValues(['Sim, na maioria', 'Em algumas', 'Quase nenhuma', 'Não sei']).setRequired(true);
  form.addGridItem().setTitle('6) Na sua região, como é o acesso a:')
      .setRows(['Saúde', 'Escolas', 'Ônibus', 'Comércio', 'Praças / áreas verdes', 'Segurança'])
      .setColumns(ESCALA).setRequired(true);
  form.addCheckboxItem().setTitle('7) O que MAIS falta na sua região? (marque até 2)')
      .setChoiceValues(['Saúde', 'Escolas', 'Transporte / ônibus', 'Comércio',
                        'Praças / áreas verdes', 'Calçadas e acessibilidade', 'Iluminação', 'Segurança']);
  form.addMultipleChoiceItem().setTitle('8) Você ou alguém da sua casa tem deficiência ou mobilidade reduzida?')
      .setChoiceValues(['Sim', 'Não', 'Prefiro não dizer']);

  var ss = SpreadsheetApp.create('CityLens — respostas (pesquisa rápida)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log('Responder: ' + form.getPublishedUrl());
  Logger.log('Editar:    ' + form.getEditUrl());
  Logger.log('Planilha:  ' + ss.getUrl());
}
