/* ============================================================
 * router.js — Reference Hash-Based Router
 * ============================================================
 * URL: dashboard.html#/home
 * Routes are registered in ROUTES, dispatched by parseHash().
 * ============================================================ */

const ROUTES = {
  'home': { render: PageHome.render, label: '舆情总览' },
  'community-sentiment': { render: PageCommunitySentiment.render, label: '官方社区舆情' },
  'external-sentiment': { render: PageExternalSentiment.render, label: '外部舆情' },
  'keywords': { render: PageKeywords.render, label: '关键词追踪' },
};

const Router = {
  parseHash() {
    const h = location.hash.replace(/^#\/?/, '');
    return h || 'home';
  },

  navigate(route) {
    if (!ROUTES[route]) route = 'home';

    // Reset platform filter per page
    STATE.currentRoute = route;
    if (route === 'community-sentiment') {
      STATE.currentPlatform = 'all';
    } else if (route === 'external-sentiment') {
      STATE.currentPlatform = 'all';
    } else {
      STATE.currentPlatform = 'all';
    }

    // Destroy any existing chart instances
    if (typeof Utils !== 'undefined' && Utils.destroyAllCharts) {
      Utils.destroyAllCharts();
    }

    const main = document.getElementById('main-content');
    main.innerHTML = '';
    main.scrollTop = 0;

    // Update active nav state
    document.querySelectorAll('.nav-item[data-route]').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });

    // Render the page; expose re-render for date/platform changes
    try {
      ROUTES[route].render(main);
      window.__reRenderCurrent = () => {
        if (Utils.destroyAllCharts) Utils.destroyAllCharts();
        main.innerHTML = '';
        main.scrollTop = 0;
        ROUTES[route].render(main);
      };
    } catch (e) {
      console.error(e);
      main.innerHTML = `<div class="empty-state"><div class="icon">⚠️</div>渲染失败：${e.message}</div>`;
    }
  },

  init() {
    window.addEventListener('hashchange', () => Router.navigate(Router.parseHash()));
    Router.navigate(Router.parseHash());
  },
};
