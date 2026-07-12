/**
 * Minecraft Style Pixel Button Web Component
 * Repository: minecraftbutton
 */
class MinecraftButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  // 모니터링할 어트리뷰트 정의
  static get observedAttributes() {
    return ['bg-top', 'bg-bottom', 'text-color', 'width', 'height'];
  }

  // 어트리뷰트 값이 변경되면 실시간으로 리렌더링
  attributeChangedCallback() {
    this.render();
  }

  connectedCallback() {
    this.render();
  }

  render() {
    // 1. 커스텀 속성값 정의 (기본값 설정)
    const bgTop = this.getAttribute('bg-top') || '#1cb853';
    const bgBottom = this.getAttribute('bg-bottom') || '#0f8b3e';
    const textColor = this.getAttribute('text-color') || '#ffffff';
    const width = this.getAttribute('width') || '312px';
    const height = this.getAttribute('height') || '60px';

    // 2. 외부 색상 기반으로 입체감 음영(Shadow) 색상 자동 계산 (원래 비율 매칭)
    // 좀 더 정밀한 제어를 원하시면 이 부분도 어트리뷰트로 분리할 수 있습니다.
    const shadowLight = '#1bc258';
    const shadowDark = '#0b662e';
    const shadowActiveLight = '#139e48';
    const shadowActiveDark = '#053b1a';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: inline-block;
          width: ${width};
          height: ${height};
        }

        .mc-pixel-button {
          display: inline-flex; 
          align-items: center; 
          justify-content: center; 
          width: 100%; 
          height: 100%; 
          
          /* 가변 수직 그라데이션 적용 */
          background: linear-gradient(180deg, ${bgTop} 0%, ${bgBottom} 100%); 
          
          color: ${textColor}; 
          font-size: calc(${height} * 0.4); /* 높이에 비례하는 가변 폰트 사이즈 */
          font-weight: 500; 
          text-decoration: none; 
          cursor: pointer; 
          user-select: none;
          box-sizing: border-box;
          position: relative;
          
          /* 3px 정사각형 픽셀 테두리 */
          border-style: solid;
          border-width: 3px 0;
          border-color: #000000;
          
          box-shadow: inset -3px -3px 0px 0px ${shadowDark}, inset 3px 3px 0px 0px ${shadowLight};
          text-shadow: 2px 2px 0px #000000;
          padding-top: 0px;
          font-family: inherit;
        }

        /* 측면 보더 및 코너 픽셀 조각 */
        .side-border {
          position: absolute; 
          top: 0; 
          bottom: 0; 
          width: 3px; 
          background-color: #000000;
        }
        .side-border.left { left: -3px; top: 3px; bottom: 3px; }
        .side-border.right { right: -3px; top: 3px; bottom: 3px; }

        .corner-pixel {
          position: absolute;
          width: 3px;
          height: 3px;
          background-color: #000000;
        }
        .corner-pixel.tl { top: 0; left: 0; }
        .corner-pixel.tr { top: 0; right: 0; }
        .corner-pixel.bl { bottom: 0; left: 0; }
        .corner-pixel.br { bottom: 0; right: 0; }

        /* =======================================================
           [클릭 상태 (Active)] 테두리 화이트 및 수직 그라데이션 반전
           ======================================================= */
        .mc-pixel-button:active {
          border-color: #ffffff;
          
          /* 그라데이션 수직 반전 (to top 구조) */
          background: linear-gradient(0deg, ${bgTop} 0%, ${bgBottom} 100%); 
          
          box-shadow: inset 3px 3px 0px 0px ${shadowActiveDark}, inset -3px -3px 0px 0px ${shadowActiveLight};
          padding-top: 3px; 
        }

        .mc-pixel-button:active .side-border,
        .mc-pixel-button:active .corner-pixel {
          background-color: #ffffff;
        }
      </style>

      <div class="mc-pixel-button">
        <span class="side-border left"></span>
        <span class="side-border right"></span>
        <span class="corner-pixel tl"></span>
        <span class="corner-pixel tr"></span>
        <span class="corner-pixel bl"></span>
        <span class="corner-pixel br"></span>
        <slot>Button</slot> </div>
    `;
  }
}

// <mc-button> 이라는 커스텀 태그로 브라우저에 등록
customElements.define('mc-button', MinecraftButton);
