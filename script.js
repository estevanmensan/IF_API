/* Dashboard HortIf — lê o dados.json gerado pelo Python (dados DIÁRIOS).
   Para voltar aos dados simulados, use: const ARQUIVO_JSON = null; */
const ARQUIVO_JSON = "dados.json";

async function carregarJson() {
  const r = await fetch(ARQUIVO_JSON + "?t=" + Date.now()); // ?t= evita cache antigo
  if (!r.ok) throw new Error("Não foi possível ler " + ARQUIVO_JSON + " (HTTP " + r.status + ")");
  return await r.json();
}

async function buscarDados() {
  if (ARQUIVO_JSON) {
    const dados = await carregarJson();
    return dados.historico;
  }
  return gerarDadosSimulados();
}

async function buscarEtc() {
  if (ARQUIVO_JSON) {
    const dados = await carregarJson();
    return dados.etc;
  }
  return { et0: 4.8, culturas: { alface: 0.9, tomate: 1.05, couve: 0.95 } };
}

function gerarDadosSimulados() {
  const registros = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    registros.push({
      data: d.toISOString().slice(0, 10),
      temperatura: +(20 + Math.random() * 5).toFixed(1),
      umidade_rel: +(60 + Math.random() * 15).toFixed(1),
      vento_2m: +(1 + Math.random()).toFixed(1),
      radiacao_mj: +(14 + Math.random() * 6).toFixed(2),
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
  const labels = registros.map(r => r.data.slice(5).split('-').reverse().join('/')); // "05/10"
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
  corpo.innerHTML = registros.slice().reverse().map(r => `
    <tr>
      <td>${r.data.split('-').reverse().join('/')}</td>
      <td>${r.temperatura}</td>
      <td>${r.umidade_rel}</td>
      <td>${r.vento_2m}</td>
      <td>${r.radiacao_mj}</td>
    </tr>`).join('');
}

function preencherEtc(dados) {
  document.getElementById('vEt0').textContent = Number(dados.et0).toFixed(1);
  const corpo = document.getElementById('corpoEtc');
  corpo.innerHTML = Object.entries(dados.culturas).map(([cultura, kc]) => `
    <tr><td>${cultura}</td><td class="num">${kc}</td><td class="num">${(dados.et0 * kc).toFixed(2)}</td></tr>
  `).join('');
}

async function iniciar() {
  try {
    const registros = await buscarDados();
    const ultimo = registros[registros.length - 1];
    document.getElementById('vTemp').innerHTML = ultimo.temperatura + '<span class="unidade">°C</span>';
    document.getElementById('vUmid').innerHTML = ultimo.umidade_rel + '<span class="unidade">%</span>';
    document.getElementById('vVento').innerHTML = ultimo.vento_2m + '<span class="unidade">m/s</span>';
    document.getElementById('vRad').innerHTML = ultimo.radiacao_mj + '<span class="unidade">MJ/m²</span>';

    montarGrafico(registros);
    preencherHistorico(registros);
    preencherEtc(await buscarEtc());
  } catch (erro) {
    console.error("Erro ao montar o dashboard:", erro);
  }
}

iniciar();