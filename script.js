
const ARQUIVO_JSON = "dados.json";

async function buscarDados() {
  if (ARQUIVO_JSON) {
    const r = await fetch(ARQUIVO_JSON);
    const dados = await r.json();
    return dados.historico;
  }
  return gerarDadosSimulados();
}

async function buscarEtc() {
  if (ARQUIVO_JSON) {
    const r = await fetch(ARQUIVO_JSON);
    const dados = await r.json();
    return dados.etc;
  }
  return { et0: 4.8, culturas: { alface: 0.9, tomate: 1.05, couve: 0.95 } };
}

function gerarDadosSimulados() {
  const agora = new Date();
  const registros = [];
  for (let i = 23; i >= 0; i--) {
    const hora = new Date(agora - i * 3600 * 1000);
    const fase = (hora.getHours() - 12) / 12;
    registros.push({
      timestamp: hora.toISOString(),
      temperatura: +(21 + 5 * Math.cos(fase * Math.PI / 1.3)).toFixed(1),
      umidade_relativa: +(65 - 15 * Math.cos(fase * Math.PI / 1.3)).toFixed(0),
      vento_2m: +(1.2 + Math.random()).toFixed(1),
      radiacao_mj: Math.max(0, Math.round(380 * Math.cos(fase * Math.PI / 1.4))),
    });
  }
  return registros;
}

let modoAutonomo = true;
function alternarModo() {
  modoAutonomo = !modoAutonomo;
  document.getElementById('dotModo').className = 'dot' + (modoAutonomo ? '' : ' manual');
  document.getElementById('textoModo').textContent = modoAutonomo ? 'Modo autônomo' : 'Modo manual';
}

let grafico;
function montarGrafico(registros) {
  const ctx = document.getElementById('graficoClima');
  const labels = registros.map(r => r.data.slice(5).split('-').reverse().join('/'));
  grafico = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Temperatura (°C)', data: registros.map(r => r.temperatura),
          borderColor: '#9C6B4A', backgroundColor: 'transparent', tension: 0.3, yAxisID: 'y' },
        { label: 'Umidade (%)', data: registros.map(r => r.umidade_rel),
          borderColor: '#4C7A93', backgroundColor: 'transparent', tension: 0.3, yAxisID: 'y1' },
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: { position: 'left', title: { display: true, text: '°C' } },
        y1: { position: 'right', title: { display: true, text: '%' }, grid: { drawOnChartArea: false } },
      }
    }
  });
}

function preencherHistorico(registros) {
  const corpo = document.getElementById('corpoHistorico');
  corpo.innerHTML = registros.slice(-8).reverse().map(r => `
    <tr>
      <td>${r.data.split('-').reverse().join('/')}</td>
      <td>${r.temperatura}</td>
      <td>${r.umidade_rel}</td>
      <td>${r.vento_2m}</td>
      <td>${r.radiacao_mj}</td>
    </tr>`).join('');
}

function preencherEtc(dados) {
  document.getElementById('vEt0').textContent = dados.et0.toFixed(1);
  const corpo = document.getElementById('corpoEtc');
  corpo.innerHTML = Object.entries(dados.culturas).map(([cultura, kc]) => `
    <tr><td>${cultura}</td><td class="num">${kc}</td><td class="num">${(dados.et0 * kc).toFixed(2)}</td></tr>
  `).join('');
}

async function iniciar() {
  const registros = await buscarDados();
  const ultimo = registros[registros.length - 1];
  document.getElementById('vTemp').innerHTML = ultimo.temperatura + '<span class="unidade">°C</span>';
  document.getElementById('vUmid').innerHTML = ultimo.umidade_rel + '<span class="unidade">%</span>';
  document.getElementById('vVento').innerHTML = ultimo.vento_2m + '<span class="unidade">m/s</span>';
  document.getElementById('vRad').innerHTML = ultimo.radiacao_mj  + '<span class="unidade">MJ/m²</span>';

  montarGrafico(registros);
  preencherHistorico(registros);
  preencherEtc(await buscarEtc());
}

iniciar();
