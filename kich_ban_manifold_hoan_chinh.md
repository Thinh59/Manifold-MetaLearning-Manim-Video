<!-- # Kịch Bản Video: Manifold Meta-Learning
## Hướng dẫn đầy đủ — Kịch bản, Công thức, Flow hình vẽ

---

## SCENE 1 — Giới thiệu: Deep Learning và Vấn đề Overfitting

**Lời thoại:**
Machine Learning hay Deep Learning là những khái niệm mà chúng ta đã quen thuộc. Những mô hình này học chỉ một tác vụ cụ thể bằng cách ghi nhớ máy móc các đặc trưng từ dữ liệu. Điều này dẫn đến việc chúng không thể áp dụng sang tác vụ mới nhưng tương tự. Ví dụ, mô hình phân biệt chó-mèo, khi gặp ảnh chim vẫn chỉ trả ra "chó" hoặc "mèo".

**Flow hình vẽ (Manim):**
```
[Ảnh chó + Ảnh mèo]  →  [Hộp: MÔ HÌNH]  →  [Đặc trưng chó, Đặc trưng mèo]
                                                       ↑
[Ảnh chim]  →  [Hộp: MÔ HÌNH]  →  ???  →  "Chó / Mèo" (SAI!)
```
> Vẽ hoạt hình: con chó, con mèo dễ thương, con chim, hộp mô hình, dấu hỏi to màu đỏ, kết quả sai in đậm.

**Gemini Prompt (nếu cần vẽ thêm):**
> "Cute cartoon illustration: a dog and cat being fed into a machine learning 'model' box, then a bird being fed in and incorrectly labeled as 'dog/cat'. Clean 2D flat design, pastel colors, whimsical style, white background."

---

## SCENE 2 — Meta-Learning: Học Cách Học

**Lời thoại:**
Vì vậy chúng ta có một khái niệm mới là **meta-learning**: học cách học. Thay vì mỗi mô hình chỉ học một tác vụ cụ thể, meta-learning cho phép mô hình học dựa vào kinh nghiệm của các tác vụ trước để nhanh chóng thích nghi với tác vụ mới. Ví dụ: đã học phân biệt chó-mèo, khi đến tác vụ gà-vịt, mô hình đã biết cách học và học nhanh hơn nhiều.

**Flow hình vẽ:**
```
Vòng 1 - Học ban đầu:
[Ảnh chó / mèo]  →  [Mô hình θ]  →  θ = "cách học"

Vòng 2 - Học tác vụ mới:
[Ảnh gà / vịt]  →  [Mô hình θ]  →  θ' (⚡ học nhanh hơn nhiều!)
```
> Vẽ chuyển động: ảnh động con gà, con vịt bay vào mô hình. Mũi tên θ → θ' có hiệu ứng tốc độ (flash, lightning bolt).

---

## SCENE 3 — MAML: Tối Ưu Khởi Tạo Trọng Số

**Lời thoại:**
Trong đó nổi bật nhất là MAML (Model-Agnostic Meta-Learning), một phương pháp tối ưu việc khởi tạo trọng số. Nhờ học cách khởi tạo trọng số tốt nhất, mô hình chỉ cần vài bước tối ưu là có thể cho ra kết quả tốt.

**Flow hình vẽ:**
```
W₁ (ngẫu nhiên)  →  [nhiều bước lặp dài/phình to]  →  y_best
                                                              ↑
W₂ (sau meta-learning)  →  [chỉ vài bước ngắn]  ──────────┘
```
> Hai luồng hội tụ vào một điểm y_best duy nhất. Luồng W₁ vẽ nhiều mũi tên ziczac, luồng W₂ vẽ đường thẳng ngắn hơn rõ ràng.

---

## SCENE 4 — Hạn Chế: Black-Box và Chi Phí Tính Toán

**Lời thoại:**
Tuy nhiên, các mô hình meta-learning truyền thống thường dùng kiến trúc hộp đen (black-box), hiệu quả nhưng đòi hỏi dữ liệu khổng lồ và chi phí tính toán rất lớn.

**Flow hình vẽ:**
```
[Mạng neural phức tạp nhiều lớp đang chạy sôi động]
         +
[Luồng dữ liệu khổng lồ đổ vào]
         ↓
[Đồng hồ tính toán: số nhảy từ 0 → ∞, dần chuyển sang màu đỏ 🔴]
```
> Vẽ đồng hồ có kim quay vòng, số đếm tăng nhanh, viền đỏ bắt đầu sáng lên.

---

## SCENE 5 — Lấy Cảm Hứng Từ Vật Lý: Con Lắc Đơn

**Lời thoại:**
Chúng ta nghĩ đến các mô hình vật lý. Học chuyển động của con lắc đơn chỉ cần biết vài tham số: biên độ A, tần số góc ω, pha φ — và đã biết được vị trí tại mọi thời điểm.

**Công thức:**
$$x(t) = A \cos(\omega t + \varphi)$$

**Flow hình vẽ:**
```
[Con lắc đơn chuyển động]
         ↓
x(t) = A·cos(ωt + φ)
    ↗        ↑        ↖
  [A]       [ω]      [φ]
Biên độ  Tần số góc   Pha ban đầu
    ↓         ↓         ↓
[Mũi tên ra các vị trí: biên trái, cân bằng, biên phải]
```
> Zoom lần lượt vào từng tham số A, ω, φ. Mỗi tham số được đánh dấu màu khác nhau trên đồ thị dao động.

---

## SCENE 6 — LEO và Không Gian Ẩn

**Lời thoại:**
Từ mô hình vật lý này, đã có nhiều ý tưởng học **không gian ẩn** — chỉ những tham số quan trọng thay vì toàn bộ tham số dư thừa. Đó là **LEO** (Latent Embedding Optimization). Tuy nhiên, LEO vẫn dùng **hai vòng lặp lồng nhau** để tối ưu từng tác vụ, gây tốn kém.

**Flow hình vẽ:**
```
[Đám mây tham số khổng lồ θ ∈ ℝⁿθ]  →  [LEO]  →  [Không gian ẩn z ∈ ℝⁿᶻ, nz ≪ nθ]

Bên dưới:
┌──── OUTER LOOP (tối ưu γ) ────────────────────────┐
│  ┌── INNER LOOP (tối ưu ϕ cho từng tác vụ) ──┐   │
│  │   ϕ̂ = argmin L(ytr, F(utr; Pγ(ϕ)))        │   │
│  └────────────────────────────────────────────┘   │
│   ← Đạo hàm bậc 2: ∇²L (CHẬM!) →                │
└────────────────────────────────────────────────────┘
```
> Vẽ hai vòng tròn lồng nhau, vòng trong màu đỏ (inner loop), vòng ngoài màu cam (outer loop), mũi tên chỉ vào LEO phía trên.

---

## SCENE 7 — Manifold Meta-Learning: Giải Pháp Đột Phá

**Lời thoại:**
Từ những ý tưởng đó, chúng ta có **Manifold Meta-Learning** — phương pháp học không gian con đa tạp quan trọng, đồng thời loại bỏ chi phí hai vòng lặp bằng cách thay vòng lặp trong bằng một **mạng phụ trợ Hypernetwork Eψ**. Mạng này đọc toàn bộ dữ liệu tác vụ chỉ một lần và trả ra vector tham số φ.

**Công thức Encoder:**
$$\hat{\phi} = E_\psi(u_{tr}, y_{tr})$$

**Flow hình vẽ:**
```
[Dữ liệu (u_tr, y_tr)]
         ↓
[Encoder E_ψ: bi-directional GRU + Feed-forward NN]
         ↓
   φ̂ ∈ ℝⁿφ   (nφ = 20, rất nhỏ!)
```
> Vẽ hộp Encoder màu cam, mũi tên vào dữ liệu, mũi tên ra φ in đậm màu xanh lá.

**Gemini Prompt (sơ đồ kiến trúc):**
> "Clean architecture diagram: Input data (u,y) goes into an orange 'Encoder (GRU)' box, outputs a small green vector phi. Then phi goes into a blue 'Lifting Function P' box, which outputs a large red vector theta. Then theta feeds into a gray 'Base Architecture F' box to produce output y-hat. Use clear arrows and labels, white background, minimal design."

---

## SCENE 8 — Hàm Ánh Xạ Lifting và Kiến Trúc Đầy Đủ

**Lời thoại:**
Từ tham số φ, mô hình dùng một **hàm ánh xạ Lifting Pγ** để chuyển trở về chiều không gian tham số gốc θ. Bản chất: θ chỉ mang nội dung của φ; các phần còn lại thưa (sparse). Sau đó đưa vào mô hình gốc F để cho kết quả dự đoán.

**Công thức Lifting (từ paper, Section 4.5):**
$$\theta = P_\gamma(\phi) = V\phi + \theta_{bias}$$

Trong đó:
- $V \in \mathbb{R}^{n_\theta \times n_\phi}$ — ma trận ánh xạ
- $\theta_{bias} \in \mathbb{R}^{n_\theta}$ — vector bias
- $\gamma = \text{vec}(V, \theta_{bias}) \in \mathbb{R}^{n_\gamma}$, với $n_\gamma = (n_\phi + 1) \cdot n_\theta = 5124$

**Công thức dự đoán đầu ra:**
$$\hat{y}_{te} = F\!\left(u_{te};\; P_{\hat{\gamma}}(\hat{\phi})\right) = F\!\left(u_{te};\; V\hat{\phi} + \theta_{bias}\right)$$

**Công thức φ̂ đầy đủ:**
$$\hat{\phi} = E_{\hat{\psi}}(u_{tr}, y_{tr})$$

**Flow hình vẽ kiến trúc đầy đủ (Encoder-Decoder):**
```
         ┌──────────── DECODER ─────────────────┐
         │                                       │
y_tr ──→ │                  P_γ(φ̂) = Vφ̂ + θ_b  │
u_tr ──→ │  ENCODER E_ψ  ──→  LIFTING  ──→  BASE ARCH F  ──→  ŷ_te
         │                  φ̂ ∈ ℝ²⁰   θ ∈ ℝ²⁴⁴  │          ↑
         └─────────────────────────────────────-─┘     u_te ─┘
```
> Đây chính là Figure 1 trong paper. Vẽ lại dưới dạng animated Manim.

---

## SCENE 9 — Hàm Loss và Tối Ưu

**Lời thoại:**
Việc tính toán và tối ưu dựa trên hàm loss J và tối ưu hóa các tham số (γ, ψ).

**Hàm Loss J (công thức 10a và 11 trong paper):**

Dạng kỳ vọng:
$$J(\gamma, \psi) = \mathbb{E}_{p(\mathcal{D})}\left[\mathcal{L}(y_{te},\, \hat{y}_{te})\right]$$

Dạng xấp xỉ Monte Carlo (dùng trong thực tế):
$$\tilde{J}(\gamma, \psi) = \frac{1}{b} \sum_{i=1}^{b} \mathcal{L}\!\left(y_{te}^{(i)},\; F\!\left(u_{te}^{(i)},\; P_\gamma\!\left(E_\psi(u_{tr}^{(i)}, y_{tr}^{(i)})\right)\right)\right)$$

Trong đó $\mathcal{L}$ thường là MSE:
$$\mathcal{L}(y, \hat{y}) = \frac{1}{N}\sum_{k=1}^{N} \|y_k - \hat{y}_k\|_2^2$$

**Tối ưu:**
$$(\hat{\gamma}, \hat{\psi}) = \arg\min_{\gamma,\, \psi}\; \tilde{J}(\gamma, \psi)$$

**Flow hình vẽ:**
```
J(γ, ψ)  →  argmin  →  (γ̂, ψ̂)
               ↑
       Gradient descent (Adam)
       batch size b=128
       lr = 2×10⁻⁴ → 2×10⁻⁵
```

---

## SCENE 10 — Phân Phối Dữ Liệu Meta p(D)

**Lời thoại:**
Một điều quan trọng trong meta-learning nói chung và Manifold nói riêng: tập dữ liệu meta **D** gồm nhiều tập con **D⁽ⁱ⁾** bên trong. Các tập con này phải tuân theo phân phối **p(D)** — nếu không, mô hình sẽ học/dự đoán kém hiệu quả hơn.

**Công thức phân phối dữ liệu (công thức 2 trong paper):**
$$p(\mathcal{D}) = p(u, y) = p(u) \int_z p(z)\, p(y \mid u, z)\; dz$$

Trong đó:
- $z \in \mathbb{R}^{n_z}$ — biến ẩn đặc trưng cho từng hệ thống (ví dụ: tham số vật lý)
- $p(z)$ — phân phối của các hệ thống trong tập meta
- $p(y \mid u, z)$ — cơ chế sinh dữ liệu của hệ thống tương ứng với $z$
- $p(u)$ — phân phối của tín hiệu đầu vào (giống nhau cho tất cả)

**Flow hình vẽ:**
```
p(z) → z⁽¹⁾, z⁽²⁾, ..., z⁽ⁿ⁾   (các hệ thống khác nhau)
p(u) → u⁽¹⁾, u⁽²⁾, ..., u⁽ⁿ⁾   (tín hiệu vào)
              ↓
   p(y|u,z) → y⁽¹⁾, y⁽²⁾, ..., y⁽ⁿ⁾
              ↓
D = {D⁽ⁱ⁾} = {(u⁽ⁱ⁾, y⁽ⁱ⁾)} ~ p(D)
```

---

## SCENE 11 — Mô Hình F là gì? (Neural State-Space)

**Lời thoại:**
Mô hình cơ sở F trong bài báo là một **Neural State-Space Model** — mô hình không gian trạng thái dùng mạng neural.

**Công thức (công thức 12 và 14 trong paper):**

Dạng tổng quát:
$$x_{k+1} = f(x_k, u_k;\, \theta), \qquad y_k = g(x_k, u_k;\, \theta)$$

Dạng cụ thể (Linear + nonlinear neural correction):
$$x_{k+1} = Ax_k + Bu_k + N_f(x_k, u_k;\, W_f)$$
$$y_k = Cx_k + N_g(x_k;\, W_g)$$

Trong đó:
- $x_k \in \mathbb{R}^3$ — vector trạng thái (ẩn)
- $N_f, N_g$ — feed-forward NN với 1 hidden layer, 16 units, activation tanh
- $\theta = \text{vec}(W_f, W_g, A, B, C) \in \mathbb{R}^{244}$

**Flow hình vẽ:**
```
u_k ──→ [   f(x,u; θ)   ] ──→ x_{k+1}
x_k ──┘         ↓
              g(x,u; θ)
                 ↓
               y_k = ŷ_k
```

---

## SCENE 12 — Kết Quả Thực Nghiệm: nφ = 10 vs nφ = 20

**Lời thoại:**
Kết quả thực nghiệm cho thấy hiệu quả vượt trội khi dùng nφ = 20 so với nφ = 10. Với dữ liệu lớn, 10 chiều quá nhỏ để nắm bắt hết sự đa dạng. Với dữ liệu rất nhỏ (L=100), 10 chiều lại tốt hơn vì tránh overfit — nhưng 20 chiều vẫn vượt trội khi dữ liệu tăng lên.

**Số liệu từ paper (Figure 3):**
- L = 500 mẫu: nφ=20 đạt median **FIT = 95.2%**, rmse = 3.18×10⁻⁵
- Full-order với L ≤ 400: median FIT **dưới baseline tuyến tính 77.2%**
- nφ=10 tốt hơn chỉ khi L = 100

**Flow hình vẽ:**
```
DỮ LIỆU LỚN:
[Data khổng lồ] → [φ₁₀: phễu quá nhỏ, bị tắc nghẽn 🔴] → kém

[Data khổng lồ] → [φ₂₀: phễu vừa đủ ✅] → tốt

DỮ LIỆU RẤT NHỎ (L=100):
[Data nhỏ] → [φ₁₀] → output y clone (ghi nhớ nguyên vẹn — overfit)
[Data nhỏ] → [φ₂₀] → output y tổng quát hóa (học cấu trúc)
```

---

## SCENE 13 — Hybrid: Encoder khởi tạo + AdamW tinh chỉnh

**Lời thoại:**
Dù Manifold cho kết quả tốt, so với hai vòng lặp truyền thống vẫn chưa hoàn toàn vượt trội. Vì vậy, họ dùng mạng Hypernetwork Eψ như một bước **khởi tạo thông minh**, rồi dùng **AdamW** để tinh chỉnh thêm vài bước — cho kết quả tốt hơn trong inference.

**Flow hình vẽ:**
```
Dữ liệu mới D* = (u*, y*)
         ↓
E_ψ̂(u*, y*) → φ₀ (khởi tạo thông minh)
         ↓
AdamW (vài bước, ~ 10000 iterations)
         ↓
φ̂* = argmin L(y*, F(u*; P_γ̂(φ)))
         ↓
ŷ* = F(u*; P_γ̂(φ̂*))
```

---

## SCENE 14 — Hình Đa Tạp (Manifold Visualization)

**Gemini Prompt để vẽ hình Manifold:**
> "Mathematical visualization of a 2D manifold embedded in 3D parameter space. Show a curved surface (like a ribbon or curved sheet) floating inside a larger 3D cube representing high-dimensional parameter space. Multiple colored dots are scattered on the manifold surface, each representing a different physical system. The manifold should glow softly in teal/green. The surrounding parameter space is dark blue. Label the manifold as 'M ⊂ ℝⁿθ' and add a small coordinate system showing nφ << nθ. Scientific visualization style, elegant, dark background."

---

## TÓM TẮT THỨ TỰ SCENE (Logic Flow)

```
S1: DL overfitting (chó/mèo/chim)
 ↓
S2: Meta-learning ra đời (học cách học)
 ↓
S3: MAML — khởi tạo trọng số tốt
 ↓
S4: Hạn chế: black-box, tốn kém
 ↓
S5: Cảm hứng vật lý (con lắc, ít tham số)
 ↓
S6: LEO — không gian ẩn, vẫn còn 2 vòng lặp
 ↓
S7: Manifold Meta-Learning + Encoder Eψ (xóa inner loop)
 ↓
S8: Lifting Pγ — chuyển φ → θ
 ↓
S9: Hàm loss J và tối ưu (γ̂, ψ̂)
 ↓
S10: Phân phối p(D) — yêu cầu dữ liệu meta
 ↓
S11: Mô hình F là Neural State-Space
 ↓
S12: Kết quả: nφ=20 tốt hơn nφ=10
 ↓
S13: Hybrid: Encoder khởi tạo + AdamW
 ↓
S14: Kết luận và tương lai
``` -->

# Kịch Bản Video v2: Manifold Meta-Learning
## Đầy đủ Formulation + Phương pháp luận (theo yêu cầu thầy)

---

## TỔNG QUAN BÀI TOÁN (Formulation chung)

**Bài toán:** Supervised regression trên time series  
- **Input:** chuỗi tín hiệu điều khiển $u_{0:N-1} \in \mathbb{R}^{n_u}$  
- **Output:** chuỗi đầu ra $y_{0:N-1} \in \mathbb{R}^{n_y}$  
- **Môi trường:** Tập meta-dataset $\mathcal{D} = \{D^{(i)}\}$ gồm nhiều dataset từ **cùng lớp hệ thống** nhưng **khác tham số vật lý**  
- **Mục tiêu:** Học một kiến trúc giảm chiều chung cho cả lớp, để inference trên hệ thống mới **nhanh và ít dữ liệu**

---

## SCENE 1 — Formulation: Vấn đề của Deep Learning

**Lời thoại:**
Trong Machine Learning, bài toán supervised learning đặt ra như sau: cho input x và nhãn y, ta tìm mô hình f-theta tối thiểu hóa loss. Deep learning rất mạnh — nhưng nó học **từ đầu** cho mỗi tác vụ, tối ưu toàn bộ theta thuộc R-n-theta từ khởi tạo ngẫu nhiên. Hệ quả: cần rất nhiều dữ liệu và không tái sử dụng được kinh nghiệm từ tác vụ trước. Ví dụ: mô hình học phân biệt chó-mèo — khi gặp chim, nó không biết gì cả.

**Formulation được nêu:**
$$\hat{\theta} = \arg\min_{\theta} \mathcal{L}(y, F(u;\theta)) + r(\theta), \quad \theta \in \mathbb{R}^{n_\theta}$$

Vấn đề: tối ưu từ đầu cho mỗi tác vụ → không kế thừa, không generalize.

**Flow hình vẽ:**
```
[Input x] → [f_θ: học từ đầu mỗi lần] → [Output ŷ]
                    ↑
         θ ∈ ℝⁿθ khởi tạo ngẫu nhiên

[Tác vụ 1: chó/mèo] → θ₁ (học xong, vứt)
[Tác vụ 2: chim??]  → θ₂ (học lại từ đầu!)  ← LÃNG PHÍ
```

---

## SCENE 2 — Meta-Learning: Formulation mới

**Lời thoại:**
Meta-learning đặt lại bài toán: thay vì tối ưu theta cho từng tác vụ đơn lẻ, ta tối ưu **omega — tham số học cách học** — trên toàn bộ phân phối tác vụ p(T). Cụ thể: omega là thứ giúp mô hình, khi gặp tác vụ mới, chỉ cần **vài bước gradient** là đạt kết quả tốt. Đây là vòng lặp ngoài học omega trên nhiều tác vụ nguồn, vòng lặp trong thích nghi theta cho từng tác vụ cụ thể.

**Formulation:**
$$\omega^* = \arg\min_\omega \mathbb{E}_{T \sim p(T)}\left[\mathcal{L}(D^{val}; \theta^*(omega))\right]$$
$$\text{s.t. } \theta^*(omega) = \arg\min_\theta \mathcal{L}(D^{tr}; \theta, \omega)$$

**Flow hình vẽ:**
```
Meta-training (outer):  học omega trên nhiều tác vụ T⁽¹⁾, T⁽²⁾, ...
                                    ↓
Inner loop (per task):  theta_i = G(omega, D_tr^(i))   [vài bước gradient]
                                    ↓
Meta-test:  theta* trên tác vụ mới T* — học NHANH hơn nhờ omega
```

---

## SCENE 3 — MAML: Phương pháp & Lý luận

**Lời thoại:**
MAML — Model-Agnostic Meta-Learning — chọn omega chính là **điểm khởi tạo theta-0** tối ưu. Lý luận: nếu tồn tại một theta-0 sao cho gradient descent chỉ cần vài bước từ đó là đến theta tốt cho bất kỳ tác vụ nào, thì ta đã học được cấu trúc chung. Tuy nhiên, để tối ưu theta-0, phải tính gradient qua cả vòng lặp trong — tức là **đạo hàm của đạo hàm, bậc hai**. Đây là nút thắt cổ chai về tính toán và bộ nhớ.

**Formulation MAML:**
$$\theta_0^* = \arg\min_{\theta_0} \sum_{T_i} \mathcal{L}_{T_i}\!\left(\theta_0 - \alpha \nabla_{\theta_0}\mathcal{L}_{T_i}(\theta_0)\right)$$

**Lý luận tại sao tốn kém:**
- Gradient update: $\theta_i' = \theta_0 - \alpha \nabla \mathcal{L}_{T_i}(\theta_0)$
- Meta-gradient: $\nabla_{\theta_0} \mathcal{L}(\theta_i')$ → cần **∇²L** (Hessian-vector product)
- Với $n_\theta = 244$: ma trận Hessian $244 \times 244$ → tính toán và lưu trữ rất lớn

**Flow hình vẽ:**
```
theta_0 (cần học)
    ↓  [inner: vài bước gradient descent]
theta_i' (đặc thù cho tác vụ i)
    ↓  [outer: cần ∇²L để cập nhật theta_0]
theta_0 ← theta_0 - beta * ∇_{theta_0} L(theta_i')
                              ↑
                    PHẢI ĐI QUA CẢ INNER LOOP → ∇²L
```

---

## SCENE 4 — Hạn chế Black-Box: Lý luận chi phí

**Lời thoại:**
Vấn đề cốt lõi không chỉ là MAML. Mọi phương pháp black-box đều gặp chung một nghịch lý: mô hình càng nhiều tham số thì càng biểu đạt tốt — nhưng chi phí tính toán tăng theo bậc hai với số tham số khi dùng second-order optimization. Và khi dữ liệu ít, overfit nặng vì không gian theta quá lớn so với thông tin có trong dữ liệu. Đây là lý do chúng ta cần một không gian tham số **nhỏ hơn nhưng vẫn đủ biểu đạt**.

**Lý luận hình thức:**
- Chiều tham số $n_\theta = 244 \gg n_z$ (số biến vật lý thực sự thay đổi)
- Eigenvalue của Hessian tại nghiệm: đa số **xấp xỉ 0** → mô hình over-parameterized
- Kết luận: không gian $\mathbb{R}^{244}$ dư thừa — chỉ cần một **subspace nhỏ** là đủ

**Flow hình vẽ:**
```
[Eigenvalue Hessian]

index:  0   50  100  150  200  244
value: [★★  ·   ·    ·    ·    · ]
        ↑
  Chỉ vài eigenvalue lớn
  → Phần lớn chiều là DƯ THỪA
  → ý tưởng: học subspace thay vì toàn bộ ℝ²⁴⁴
```

---

## SCENE 5 — Cảm Hứng Vật Lý: Lý luận về chiều thực sự

**Lời thoại:**
Hãy nhìn vào mô hình vật lý. Con lắc đơn có vô số trạng thái có thể — nhưng toàn bộ hành vi được xác định hoàn toàn bởi **ba số**: biên độ A, tần số góc omega, và pha phi. Đây là ví dụ của một hệ có **chiều nội tại thấp** dù không gian quan sát cao chiều. Tương tự, lớp hệ thống Bouc-Wen có 8 tham số vật lý biến đổi — trong khi mô hình neural có 244 tham số. Nếu ta học được **không gian 20 chiều** phản ánh đúng sự biến đổi thực sự, thì 244 chiều còn lại là dư thừa và không cần tối ưu.

**Công thức:**
$$x(t) = A\cos(\omega t + \varphi) \quad \Rightarrow \quad n_z = 3 \ll n_{\text{trạng thái}}$$

**Lý luận:**
- Hệ thống vật lý: $z \in \mathbb{R}^{n_z}$ (ít) → $\theta \in \mathbb{R}^{n_\theta}$ (nhiều) 
- Tồn tại ánh xạ $P^\dagger: \mathbb{R}^{n_z} \to \mathbb{R}^{n_\theta}$: mỗi hệ thống $z$ → một $\theta$ tốt
- Mục tiêu: học $P^\dagger$ này từ dữ liệu, không cần biết $z$ tường minh

---

## SCENE 6 — LEO: Tiến bộ và Hạn chế còn lại

**Lời thoại:**
LEO — Latent Embedding Optimization — đã đi đúng hướng: học không gian ẩn z nhỏ hơn, rồi decode ra theta. Lý luận của LEO: thay vì tối ưu theta trong R-244, tối ưu z trong R-20 rồi decode — bề mặt loss phẳng hơn, gradient rõ ràng hơn. **Nhưng LEO vẫn giữ inner loop**: với mỗi tác vụ, vẫn chạy gradient descent trong không gian ẩn z để tìm z tốt nhất. Điều này vẫn đòi hỏi tính đạo hàm bậc hai qua inner loop — chậm khi số tác vụ meta lớn.

**Formulation LEO:**
$$\hat{z}_i = \arg\min_z \mathcal{L}(F(u_{tr}; g_{\phi_d}(z)), y_{tr}) \quad \text{[inner loop — vẫn cần!]}$$
$$\gamma \leftarrow \gamma - \eta \nabla_\gamma \sum_i \mathcal{L}(F(u_{te}; g_{\phi_d}(\hat{z}_i)), y_{te}) \quad \text{[outer loop]}$$

**Lý luận điểm yếu còn lại:**
- Inner loop vẫn chạy nhiều bước gradient cho **mỗi** tác vụ
- Meta-gradient phải đi xuyên qua inner loop → vẫn cần $\nabla^2 \mathcal{L}$
- $n_z$ lần nhỏ hơn nhưng vẫn O(n_z²) cho second-order

**Flow hình vẽ:**
```
LEO:
┌─────── OUTER LOOP: tối ưu γ (encoder+decoder params) ──────────┐
│  ┌── INNER LOOP: tối ưu z cho TỪNG tác vụ (gradient) ──┐       │
│  │   ẑ = argmin L(F(u_tr; g(z)), y_tr)                  │       │
│  │   ← CẦN ∇²L qua đây →                                │       │
│  └────────────────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────────────────┘
Vẫn tốn kém! Chỉ giảm chiều không gian, KHÔNG giảm số vòng lặp.
```

---

## SCENE 7 — Manifold: Giải pháp loại bỏ Inner Loop

**Lời thoại:**
Manifold Meta-Learning đặt câu hỏi: có nhất thiết phải dùng gradient descent để tìm phi-hat cho mỗi tác vụ không? Câu trả lời là không — nếu ta học được một hàm trực tiếp từ dữ liệu sang phi. Đây là ý tưởng cốt lõi: thay inner loop optimization bằng một **mạng Encoder E-psi** — một multiparametric solution học sẵn cách đọc dataset và xuất ra phi chỉ trong một lần forward pass. Không có gradient lặp, không có second-order derivative. Chi phí inference giảm từ O(K * n_z²) xuống O(1) forward pass.

**Formulation Encoder:**
$$\hat{\phi} = E_\psi(u_{tr}, y_{tr}) \in \mathbb{R}^{n_\phi} \quad \text{[một lần forward — thay toàn bộ inner loop]}$$

**Lý luận tại sao hợp lý:**
- $E_\psi$ là **multiparametric solution** của bài toán inner optimization
- Thay vì solve optimization mỗi lần (expensive), amortize chi phí vào meta-training
- Sau khi train xong, inference = 1 forward pass qua GRU + MLP

**Flow hình vẽ:**
```
LEO:         [Task data] → [gradient × K bước] → ẑ
Manifold:    [Task data] → [E_ψ: 1 forward pass] → φ̂

Chi phí:     O(K · n_z²)   →   O(1)   ✅
```

---

## SCENE 8 — Lifting: Từ φ về θ và Kiến Trúc Đầy Đủ

**Lời thoại:**
Từ phi-hat 20 chiều, ta cần tạo ra theta 244 chiều để đưa vào mô hình F. Hàm Lifting tuyến tính được chọn: theta bằng V nhân phi cộng theta-bias. Tại sao tuyến tính? Vì manifold tuyến tính — affine subspace — đủ biểu đạt cho lớp hệ thống Bouc-Wen, đồng thời gradient flow tốt và không thêm nonlinearity phức tạp. Toàn bộ kiến trúc là encoder-decoder: encoder E-psi đọc dữ liệu train và xuất phi, decoder gồm Lifting rồi F xuất dự đoán trên dữ liệu test.

**Công thức Lifting:**
$$\theta = P_\gamma(\phi) = V\phi + \theta_{\text{bias}}, \quad V \in \mathbb{R}^{244 \times 20},\; \theta_{\text{bias}} \in \mathbb{R}^{244}$$
$$\gamma = \text{vec}(V, \theta_{\text{bias}}) \in \mathbb{R}^{5124}$$

**Công thức dự đoán:**
$$\hat{y}_{te} = F\!\left(u_{te};\; V\hat{\phi} + \theta_{\text{bias}}\right)$$

**Lý luận chọn linear lifting:**
- $\mathcal{M} = \{V\phi + \theta_{bias} : \phi \in \mathbb{R}^{20}\}$ là **affine subspace** 20D trong $\mathbb{R}^{244}$
- Linear đủ vì: sự biến đổi giữa các hệ thống Bouc-Wen là **smooth và low-dimensional**
- Gradient của loss qua $P_\gamma$ là constant w.r.t $\phi$ → tối ưu ổn định hơn

**Kiến trúc đầy đủ:**
```
(y_tr, u_tr) → [ENCODER E_ψ] → φ̂ ∈ ℝ²⁰
                                  ↓
                           [LIFTING P_γ]  →  θ ∈ ℝ²⁴⁴
                                  ↓
                u_te →    [BASE ARCH F]   →  ŷ_te
```

---

## SCENE 9 — Hàm Loss và Tối Ưu

**Lời thoại:**
Toàn bộ hệ thống được huấn luyện end-to-end qua hàm loss J tính trung bình Monte Carlo trên tập meta. Điểm quan trọng: ta tối ưu đồng thời cả gamma — tham số Lifting — và psi — tham số Encoder. Không có hai giai đoạn riêng biệt. Mỗi batch lấy b=128 dataset, mỗi dataset tính loss trên phần test, rồi backprop qua toàn bộ đồ thị tính toán — qua F, qua Lifting, qua Encoder — chỉ một lần.

**Hàm Loss:**
$$\tilde{J}(\gamma,\psi) = \frac{1}{b}\sum_{i=1}^{b} \mathcal{L}\!\left(y_{te}^{(i)},\; F\!\left(u_{te}^{(i)},\; P_\gamma\!\left(E_\psi(u_{tr}^{(i)}, y_{tr}^{(i)})\right)\right)\right)$$

$$(\hat{\gamma}, \hat{\psi}) = \arg\min_{\gamma,\psi}\; \tilde{J}(\gamma,\psi)$$

**Lý luận:**
- Single-level optimization: không còn bilevel như MAML/LEO
- Gradient: $\nabla_\gamma \tilde{J}$ và $\nabla_\psi \tilde{J}$ đều **first-order** — không cần Hessian
- Đây là lý do có thể dùng Adam thay vì phải dùng second-order solver

---

## SCENE 10 — Phân Phối p(D) và Yêu Cầu Dữ Liệu Meta

**Lời thoại:**
Để Manifold hoạt động, tập meta phải tuân theo phân phối p(D) đúng nghĩa. Cụ thể: mỗi dataset D trong meta được sinh bởi một hệ thống S-i, đặc trưng bởi biến ẩn z-i — trong bài toán này là tám tham số vật lý của Bouc-Wen. Nếu các hệ thống trong meta không đủ đa dạng — ví dụ toàn hệ thống giống nhau — manifold học được sẽ suy biến và không bao phủ được lớp hệ thống đích. Ngược lại, nếu quá đa dạng ngoài lớp, manifold sẽ không học được cấu trúc chung.

**Công thức:**
$$p(\mathcal{D}) = p(u)\int_z p(z)\,p(y \mid u, z)\,dz$$

**Lý luận quan trọng:**
- $z$: biến ẩn đặc trưng hệ thống, $n_z \leq n_\phi$ là điều kiện **đủ** để Problem 1 có nghiệm
- $p(z)$ phải cover đủ range biến đổi → meta-dataset cần đủ đa dạng
- Nếu $n_\phi < n_z$: manifold không đủ chiều → underfitting trên toàn lớp hệ thống

---

## SCENE 11 — Mô Hình F: Neural State-Space

**Lời thoại:**
Mô hình cơ sở F trong bài báo là Neural State-Space Model — kết hợp tuyến tính và mạng neural. Trạng thái tiếp theo bằng tổng phần tuyến tính A-x cộng B-u và phần nonlinear N-f. Đầu ra tương tự. Cấu trúc này có ưu điểm: phần tuyến tính đảm bảo gradient flow tốt và ổn định số học, phần nonlinear N-f và N-g học phần dư còn lại. Toàn bộ 244 tham số theta gồm các ma trận A, B, C và trọng số mạng Nf, Ng.

**Công thức:**
$$x_{k+1} = Ax_k + Bu_k + N_f(x_k, u_k;\,W_f)$$
$$y_k = Cx_k + N_g(x_k;\,W_g)$$
$$\theta = \text{vec}(W_f, W_g, A, B, C) \in \mathbb{R}^{244}$$

**Lý luận thiết kế:**
- $n_x = 3$: đủ để biểu diễn 3 trạng thái vật lý (p, v, z) của Bouc-Wen
- Linear backbone + nonlinear correction: cân bằng giữa biểu đạt và ổn định
- $n_\theta = 244 \gg n_z = 8$: over-parameterized → cần manifold để giảm chiều hiệu quả

---

## SCENE 12 — Kết Quả và Phân Tích

**Lời thoại:**
Kết quả thực nghiệm xác nhận lý luận. Với L=500 mẫu: reduced-order n-phi=20 đạt median FIT 95.2% — trong khi full-order với cùng dữ liệu đó vẫn dưới baseline tuyến tính 77.2%. Tại sao? Vì manifold 20 chiều đã encode prior knowledge về lớp hệ thống — optimization chỉ cần tìm 20 số thay vì 244. Với L trên 2000 mẫu, full-order bắt đầu vượt vì dữ liệu đủ để khai thác toàn bộ capacity. Đây là trade-off: data-scarce favors manifold, data-rich favors full-order.

**Số liệu từ paper:**
- L = 500: nφ=20 → median FIT **95.2%**, rmse = 3.18×10⁻⁵
- L ≤ 400: full-order median FIT **< 77.2%** (dưới baseline tuyến tính!)
- L > 2000: full-order dần vượt nhờ capacity cao hơn
- nφ=10 tốt hơn chỉ khi L=100 (quá ít dữ liệu, 20 chiều overfit)

**Lý luận:**
```
Dữ liệu ÍT:
  Full-order: 244 tham số tự do → overfit → kém
  Manifold-20: chỉ 20 tham số tự do → regularized by prior → tốt ✅

Dữ liệu NHIỀU:
  Full-order: tận dụng full capacity → tốt
  Manifold-20: bị ràng buộc bởi subspace 20D → tiệm cận giới hạn
```

---

## SCENE 13 — Hybrid: Encoder khởi tạo + AdamW tinh chỉnh

**Lời thoại:**
Encoder E-psi cho kết quả tốt nhưng chưa tối ưu — vì nó là xấp xỉ của optimization, không phải optimization thực sự. Giải pháp hybrid: dùng E-psi như một **warm start thông minh** — cho ra phi-0 gần vùng tối ưu — rồi chạy AdamW trên bài toán reduced-complexity để tinh chỉnh. Lý luận: AdamW từ phi-0 tốt hội tụ nhanh hơn nhiều so với từ khởi tạo ngẫu nhiên, và vẫn chỉ tối ưu trong không gian 20 chiều nên rẻ hơn full-order.

**Flow:**
$$D^* = (u^*, y^*) \xrightarrow{E_{\hat{\psi}}} \phi_0 \xrightarrow{\text{AdamW 10k steps}} \hat{\phi}^* = \arg\min_\phi \mathcal{L}(y^*, F(u^*; P_{\hat{\gamma}}(\phi)))$$
$$\hat{y}^* = F(u^*;\; P_{\hat{\gamma}}(\hat{\phi}^*))$$

**Lý luận:**
- Encoder: O(1) forward pass → phi_0 gần optimal
- AdamW từ phi_0: hội tụ trong ~10k bước thay vì ~50k từ random
- Toàn bộ vẫn trong ℝ²⁰ → chi phí nhỏ hơn full-order ~25%

---

## SCENE 14 — Kết Luận: Hành Trình và Tương Lai

**Lời thoại:**
Hành trình từ MAML đến Manifold là hành trình giảm thiểu chi phí tính toán mà không hi sinh biểu đạt. MAML: tối ưu trong R-n-theta với second-order gradient. LEO: giảm xuống R-n-z nhưng vẫn inner loop. Manifold: giảm xuống R-n-phi, loại bỏ hoàn toàn inner loop, thay bằng một forward pass. Mỗi bước đều có lý luận toán học rõ ràng. Trong tương lai: học phân phối xác suất trên manifold thay vì điểm — tức là variational meta-learning — sẽ cho phép uncertainty quantification. Và tích hợp phương trình vi phân vật lý vào kiến trúc F sẽ mở rộng áp dụng ra ngoài system identification.

**Timeline lý luận:**
```
MAML:     omega = theta_0,  inner = gradient descent,  cost = O(K·nθ²)
LEO:      omega = encoder+decoder, inner = gradient in z, cost = O(K·nz²)  
Manifold: omega = encoder+lifting,  inner = NONE (1 forward), cost = O(1)
                                                              ↑
                                             amortized vào meta-training
```

---

## TÓM TẮT FORMULATION & PHƯƠNG PHÁP LUẬN

| | Formulation | Phương pháp | Vì sao tốt hơn |
|---|---|---|---|
| **MAML** | omega = init, bilevel opt | gradient qua inner loop | Đơn giản nhưng ∇²L tốn kém |
| **LEO** | omega = latent space, bilevel | inner loop trong z ∈ ℝⁿᶻ | Giảm chiều nhưng vẫn inner loop |
| **Manifold** | omega = (E_ψ, P_γ), single-level | replace inner loop by E_ψ | First-order only, O(1) inference |