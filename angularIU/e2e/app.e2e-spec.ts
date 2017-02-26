import { VicomNLPHackathonNewPage } from './app.po';

describe('vicom-nlphackathon-new App', function() {
  let page: VicomNLPHackathonNewPage;

  beforeEach(() => {
    page = new VicomNLPHackathonNewPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
