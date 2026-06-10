# 디자인·구현 가이드 (5단계)

생성되는 모든 게임 HTML이 지켜야 하는 규칙. 위반 항목은 검증(6단계)에서 불합격 처리된다.

## 1. 단일 파일 + 제로 의존

- **HTML 1개 파일**에 CSS(`<style>`)와 JS(`<script>`)를 모두 인라인으로 넣는다. 외부 파일·프레임워크·빌드 도구 금지.
- **외부 네트워크 요청 금지.** Tailwind CDN, Font Awesome, 외부 이미지·아이콘·JS 라이브러리 사용 금지. 아이콘이 필요하면 이모지 또는 인라인 SVG를 쓴다.
- **유일한 예외: 구글 폰트.** 단, 차단·오프라인 환경에서도 깨지지 않도록 시스템 폰트 폴백을 반드시 지정한다.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; }
  .title { font-family: 'Jua', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; }
</style>
```

- 검증 기준: HTML 안의 `http` 문자열은 구글 폰트 도메인(fonts.googleapis.com, fonts.gstatic.com)만 허용.

## 2. 표준 head

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>게임 이름</title>
```

## 3. GAME_DATA 분리 (교사 수정 가능성)

문항·정답·해설 등 학습 데이터는 `<script>` **최상단에 하나의 상수**로 분리하고, 비개발자 교사를 위한 한국어 주석을 붙인다. 게임 로직 안에 문항을 흩어 놓지 않는다.

```javascript
// ═══════════════════════════════════════════════════
// ✏️ 문항 수정 구역 — 이 부분만 고치면 됩니다!
// 이 파일을 메모장(Windows) 또는 텍스트 편집기(Mac)로 열어
// 아래 따옴표 안의 글자만 바꾸고 저장하세요.
// 규칙: 따옴표(")와 쉼표(,)는 지우면 안 돼요.
// ═══════════════════════════════════════════════════
const GAME_DATA = {
  title: "식물 구조 탐험",          // 게임 제목
  grade: "초등 5학년 과학",         // 대상
  questions: [
    {
      q: "물과 양분의 이동 통로 역할을 하는 부분은?",  // 문제
      choices: ["뿌리", "줄기", "잎", "꽃"],           // 보기 4개
      answer: 1,                                       // 정답 번호(0부터 셈: 0=첫 번째)
      explain: "줄기는 뿌리에서 흡수한 물과 양분이 지나가는 통로예요."  // 해설
    }
  ]
};
// ═══════ 문항 수정 구역 끝 (아래는 건드리지 마세요) ═══════
```

스키마는 게임 유형별 패턴 문서를 따르되, "수정 구역" 주석 형식은 위와 동일하게 유지한다.

**패턴 문서의 스키마는 전체 옵션 카탈로그다.** 해당 게임의 variant가 실제로 사용하는 필드만 GAME_DATA에 포함한다 (예: 분류형이면 `steps` 제외, 4지선다면 OX용 필드 제외). 미사용 필드를 넣으면 검증 B6에서 불합격된다.

### 3-1. 문항 데이터 안전장치 (필수)

교사가 메모장으로 문항을 고치다 따옴표·쉼표를 지우면 문법 오류가 나고, 그러면 화면이 통째로 백지가 되어 교사가 패닉에 빠진다. 이를 막는 안전장치를 **반드시** 탑재한다.

**핵심 원칙 — 데이터와 로직을 별도 `<script>` 태그로 분리한다.** GAME_DATA와 게임 로직을 같은 `<script>` 블록에 두면, 데이터 부분에 문법 오류가 났을 때 그 블록 전체(안전장치 코드 포함)가 실행되지 않아 아무것도 못 잡는다. 다음 3개 스크립트를 **이 순서로, `</body>` 직전에** 배치한다 (head에 두면 오류 표시 시점에 `document.body`가 없어 동작하지 않는다):

```html
<!-- ❶ 오류 안전장치 — 다른 어떤 스크립트보다 먼저 둔다 -->
<script>
  window.onerror = function (msg, src, line) {
    var hint = line ? ` (파일 약 ${line}번째 줄 근처를 확인하세요)` : '';
    document.body.innerHTML =
      '<div style="max-width:560px;margin:40px auto;padding:24px;' +
      "font-family:'Noto Sans KR','Malgun Gothic',sans-serif;background:#FFF0F0;" +
      'border:3px solid #FF5555;border-radius:12px;color:#333;line-height:1.6;">' +
      '<h2 style="color:#CC0000;margin-top:0;">⚠️ 문항을 불러오지 못했어요</h2>' +
      '<p>메모장으로 문항을 고치는 과정에서 <b>따옴표(")</b>나 <b>쉼표(,)</b>가 ' +
      '지워졌을 가능성이 높아요.' + hint + '</p>' +
      '<p style="font-size:14px;color:#666;">파일을 다시 열어 수정 구역의 따옴표·쉼표를 ' +
      '확인한 뒤 저장하고, 아래 버튼을 눌러주세요.</p>' +
      '<button onclick="location.reload()" style="padding:10px 18px;background:#CC0000;' +
      'color:#fff;border:none;border-radius:6px;font-size:15px;cursor:pointer;">다시 불러오기</button>' +
      '</div>';
    return true;  // 기본 오류 처리(백지 화면) 억제
  };
</script>

<!-- ❷ 문항 데이터 — 반드시 별도 태그. 여기서 문법 오류가 나도 ❶이 줄 번호와 함께 잡아낸다 -->
<script>
  const GAME_DATA = { /* 위 "문항 수정 구역" 그대로 */ };
</script>

<!-- ❸ 게임 로직 — 데이터 누락(전역 미정의)도 한 번 더 방어 -->
<script>
  window.addEventListener('DOMContentLoaded', () => {
    if (typeof GAME_DATA === 'undefined') throw new Error('GAME_DATA를 읽지 못했습니다.');
    initApp();  // 게임 초기화 진입점
  });
</script>
```

- `window.onerror`를 가장 먼저 등록해야 ❷의 **파싱 단계 문법 오류**까지 잡는다(try-catch는 파싱 오류를 못 잡는다 — 이 점이 핵심).
- ❸의 `typeof` 검사는 데이터 스크립트가 통째로 실패해 GAME_DATA 자체가 정의되지 않은 경우에 대한 이중 방어다.

## 4. 학교급별 디자인 톤

2단계에서 파악한 학교급에 따라 자동 적용한다.

| | 초등 | 중등 | 고등 |
|---|---|---|---|
| 분위기 | 밝고 명랑한 놀이터 | 게임감 있되 절제 | 세련된 퀴즈쇼 |
| 배경 | 밝은 파스텔 또는 선명한 그라데이션 | 짙은 네이비·차콜 + 포인트색 | 다크 모드 + 금색/청록 포인트 |
| 제목 폰트 | Jua (둥근 폰트) | Jua 또는 Noto Sans KR Bold | Noto Sans KR Bold |
| 이모지 | 풍부하게 (제목·버튼·피드백) | 핵심 위치만 | 최소한 (결과 화면 정도) |
| 애니메이션 | 통통 튀는 모션, 정답 시 축하 효과 | 부드러운 전환 | 빠르고 절제된 전환 |
| 말투(게임 내 문구) | "~해 보자!", "참 잘했어요! 🎉" | "~해 보자", "정답!" | "정답입니다", 간결체 |

공통: 정답=초록 계열, 오답=빨강 계열, 대기/중립=회색. 팀전이면 팀 색을 뚜렷하게 구분(주황/파랑/초록/보라 순).

## 5. 주 활용 방식별 최적화

| | ① TV 화면 수업용 | ② 학생 개별 접속용 | ③ 전자칠판용 |
|---|---|---|---|
| 기준 화면 | 가로 1920×1080 | 세로 모바일(360~430px) 우선 | 가로 대형 터치 |
| 글자 크기 | 교실 뒤에서 보이게: 문제 본문 최소 32px, 보기 28px | 모바일 기준 문제 20px+ | 32px+ |
| 조작 주체 | 교사가 마우스/리모컨 클릭 (다음·정답 공개 버튼 크고 명확하게) | 학생 각자 터치 | 학생이 직접 터치 |
| 게임 구조 | 전체 공개형: 문제 제시 → 학생 구두 응답 → 교사가 '정답 공개' 클릭. 팀 점수판 적합 | 개인 진행형: 각자 풀고 즉시 채점, 결과 화면 | 전체 공개형 + 대형 터치 타겟(최소 80×80px), 드래그보다 탭-탭 방식 선호 |
| 추가 | 타이머는 크게 중앙 상단 | 한 손 조작 가능 배치, 입력창 포커스 시 화면 가림 주의 | 화면 하단 60%에 주요 버튼 (학생 키 닿는 위치) |

주 방식에 최적화하되, **반응형은 항상 기본 탑재**: 미디어 쿼리로 모바일 세로~대형 가로까지 레이아웃이 깨지지 않아야 한다.

**TV·전자칠판용 진행 화면은 스크롤 없이 한 화면에 수납**되어야 한다 — 진행에 필요한 버튼(정답 공개·판정·다음)이 1280×800(노트북)과 1920×1080(TV) 모두에서 뷰포트 안에 보여야 한다. 세로 여백·패딩은 `@media (max-height: ...)` 쿼리로 압축한다. **압축 쿼리의 임계값은 반드시 1080 이상으로 둘 것**(예: `max-height:1100px`) — 노트북(800)만 보고 `max-height:860px`처럼 잡으면 1920×**1080** TV에는 쿼리가 발동하지 않아, 노트북 검증은 통과하면서 TV에서만 판정 버튼이 폴드 아래로 잘리는 함정이 생긴다(특히 그림/SVG가 들어가는 문항). 압축 시 그림 높이도 상한을 두어(`max-height` 약 130px) 카드 총 높이가 뷰포트를 넘지 않게 한다. (검증 시 두 해상도에서, 그림 있는 문항으로 진행 버튼 위치를 확인할 것 — D2 연계)

글자 크기 기준의 해석:
- 위 표의 크기 기준은 **주 활용 방식의 기준 화면에서** 판정한다 (D2). 다른 폭으로 줄어들 때는 비례 축소를 허용하되 사용 가능해야 한다 (C3).
- 적용 범위: "문제 본문" 기준은 문제·낱말 카드·안내 문구 등 **학생이 읽어야 진행되는 본문 텍스트** 전체에 적용. 보기·버튼은 TV/전자칠판 28px+, 결과 화면의 복습 목록 등 보조 텍스트는 18px+ (TV/전자칠판 22px+)면 충분.

## 6. 터치·교실 환경 공통 규칙

```css
* { -webkit-tap-highlight-color: transparent; -webkit-user-select: none; user-select: none; }
input, textarea { -webkit-user-select: text; user-select: text; }
button { touch-action: manipulation; cursor: pointer; }  /* 더블탭 줌 방지 */
```

- 클릭과 터치 모두 동작해야 한다. `click` 이벤트 기본 사용 (터치에서도 발화). 드래그가 필요한 게임만 pointer 이벤트 사용.
- 우클릭 메뉴 방지는 게임 보드 영역에만 적용 (페이지 전체 금지하지 않음).

## 7. 화면 흐름 표준

```
[시작 화면] → [게임 진행] → [결과 화면]
```

- **시작 화면**: 게임 제목(`GAME_DATA.title`)과 학습 주제(`GAME_DATA.grade`)를 화면에 표시, 규칙 설명 3줄 이내, 시작 버튼. (팀전이면 팀 수/이름 설정 포함) — GAME_DATA의 모든 필드는 실제로 화면 또는 로직에서 사용돼야 한다.
- **게임 진행**: 진행 상황 표시(○/○ 문항 또는 점수판), 패턴별 게임 보드.
- **결과 화면**: 점수·등급(또는 승리 팀), **틀린 문항 다시 보기(문제+정답+해설)**, "다시 하기" 버튼. 다시 하기는 새로고침 없이 상태를 초기화해야 한다.

## 8. 학습 피드백 패턴 (필수)

- 정답: 즉각적인 긍정 피드백 (색·짧은 효과).
- **오답: 정답이 무엇인지 + 한 줄 해설을 반드시 표시**한 뒤 다음으로 진행. 해설 없이 "땡!"만 하고 넘어가는 게임은 불합격.
- 결과 화면의 "틀린 문항 다시 보기"로 복습을 마무리한다.
- 문항 순서는 매 판 섞는다 (보기 순서도 가능하면 섞되, answer 인덱스 처리 주의). 단, 패턴이 고정 배치를 요구하는 경우(예: 팀 대항 점수판의 난이도순 칸 배치)는 예외 — 패턴 문서가 우선한다.

## 9. 저장·기록

- 서버 통신 금지. 기록이 필요하면 localStorage만 사용 (최고 점수 등).
- localStorage 키는 `makelearn_게임명_*` 형식으로 충돌을 피한다.
- localStorage가 막힌 환경(file:// 일부 브라우저)에서도 게임 자체는 동작해야 한다 — try/catch로 감싼다.

## 10. 코드 품질

- 바닐라 JS, ES6+. 전역 상태는 `state` 객체 하나로 모은다.
- 화면 전환은 섹션 show/hide 방식 (SPA 라우터 불필요).
- **요소 표시/숨김은 CSS 클래스 토글(`classList.add/remove("hidden")`)로 통일한다.** `el.style.display = ""`로 '복원'하는 방식은 스타일시트에 `display: none`이 선언된 요소에서 동작하지 않는다(인라인이 비면 스타일시트 규칙이 되살아남) — 실제 진행 불가 버그의 단골 원인이므로 금지.
- 고정 위치(absolute) UI 요소(사운드 버튼 등)는 다른 화면의 같은 자리 요소와 겹치지 않는지 모든 화면 기준으로 확인한다.
- 효과음이 필요하면 Web Audio API로 간단한 비프음 생성 (외부 오디오 파일 금지). 소리 켬/끔 버튼 제공. **아래 표준 사운드 유틸을 그대로 포함해 쓴다** — 게임마다 볼륨·주파수가 제각각이 되어 학생에게 소음으로 들리는 것을 막기 위함이다. (정답·오답·클릭만 쓰면 충분하고, 더 필요한 경우만 type를 추가한다.)

```javascript
const SoundEffect = {
  enabled: true,
  ctx: null,
  play(type) {
    if (!this.enabled) return;
    try {
      if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      if (this.ctx.state === 'suspended') this.ctx.resume();  // 첫 사용자 조작 후 활성화
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.connect(gain); gain.connect(this.ctx.destination);
      const now = this.ctx.currentTime;
      if (type === 'correct') {            // 정답: 도-미-솔 상승음
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.setValueAtTime(659.25, now + 0.1);
        osc.frequency.setValueAtTime(783.99, now + 0.2);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        osc.start(now); osc.stop(now + 0.4);
      } else if (type === 'wrong') {       // 오답: 낮게 떨어지는 경고음
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.linearRampToValueAtTime(110, now + 0.3);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
        osc.start(now); osc.stop(now + 0.35);
      } else {                              // 클릭: 짧은 탭음
        osc.frequency.setValueAtTime(600, now);
        gain.gain.setValueAtTime(0.07, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
        osc.start(now); osc.stop(now + 0.08);
      }
    } catch (e) { /* 오디오 미지원 환경에서도 게임은 계속 동작 */ }
  }
};
// 사용: SoundEffect.play('correct') / .play('wrong') / .play('click')
// 켬/끔 버튼: SoundEffect.enabled = !SoundEffect.enabled
```
- 전체 분량 목표: 600~1,200줄. 과한 기능보다 핵심 규칙의 완성도에 집중한다.
