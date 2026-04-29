# manim -qh manifold_3b1b_style_1.py ManifoldMetaLearningFlow
from manim import *
import numpy as np
import os

def nn_layer(n, x, y_center, color, radius=0.14, gap=0.48):
    return VGroup(*[
        Circle(radius=radius, color=color, fill_opacity=0.85)
        .move_to([x, y_center + (i - (n-1)/2) * gap, 0])
        for i in range(n)
    ])

def nn_edges(l1, l2, color=WHITE, opacity=0.18):
    return VGroup(*[
        Line(a.get_center(), b.get_center(),
             stroke_opacity=opacity, stroke_width=1.2, color=color)
        for a in l1 for b in l2
    ])

def audio_dur(path, default=15):
    try:
        from moviepy.editor import AudioFileClip
        if os.path.exists(path):
            return AudioFileClip(path).duration
    except Exception:
        pass
    return default

class ManifoldMetaLearningFlow(Scene):
    def construct(self):
        F = "DejaVu Sans"

        dur = [
            audio_dur("audio/s01_intro.mp3",          14),
            audio_dur("audio/s02_meta_learning.mp3",  15),
            audio_dur("audio/s03_maml.mp3",           15),
            audio_dur("audio/s04_blackbox_limits.mp3",14),
            audio_dur("audio/s05_physics.mp3",        15),
            audio_dur("audio/s06_leo.mp3",            15),
            audio_dur("audio/s07_manifold_idea.mp3",  16),
            audio_dur("audio/s08_lifting.mp3",        15),
            audio_dur("audio/s09_loss.mp3",           14),
            audio_dur("audio/s10_distribution.mp3",   14),
            audio_dur("audio/s11_model_f.mp3",        14),
            audio_dur("audio/s12_results.mp3",        15),
            audio_dur("audio/s13_hybrid.mp3",         14),
            audio_dur("audio/s14_conclusion.mp3",     17),
        ]

        t = dur[0]
        title1 = Text("Supervised Learning & Hạn chế", font=F, font_size=38, color=BLUE_B).to_edge(UP)

        la = nn_layer(4, -2, 0, RED_B)
        lb = nn_layer(6, 0, 0, RED_B)
        lc = nn_layer(4, 2, 0, RED_B)
        network = VGroup(nn_edges(la,lb,RED_A), nn_edges(lb,lc,RED_A), la, lb, lc)
        network.scale(1.3).shift(DOWN*0.5)

        data_dog = Square(color=BLUE_B, fill_opacity=0.8).scale(0.6).move_to([-6, -0.5, 0])
        data_bird = Triangle(color=YELLOW_B, fill_opacity=0.8).scale(0.6).move_to([-6, -0.5, 0])
        check = MathTex(r"\checkmark", color=GREEN, font_size=80).move_to([5, -0.5, 0])
        cross = MathTex(r"\times", color=RED, font_size=100).move_to([5, -0.5, 0])
        
        self.play(Write(title1), FadeIn(network, shift=UP), run_time=t*0.1)
        self.play(FadeIn(data_dog, shift=RIGHT), run_time=t*0.1)
        self.play(data_dog.animate.move_to(network[2].get_left() + LEFT*0.5), run_time=t*0.1)
        self.play(LaggedStart(*[Indicate(layer, color=YELLOW) for layer in [network[2], network[3], network[4]]], lag_ratio=0.1), run_time=t*0.15)
        self.play(TransformFromCopy(network[4], check), run_time=t*0.1)

        self.play(FadeOut(data_dog), FadeOut(check), run_time=t*0.05)
        self.play(FadeIn(data_bird, scale=0.5), run_time=t*0.1)
        self.play(data_bird.animate.move_to(network[2].get_left() + LEFT*0.5), run_time=t*0.05)
        
        self.play(Wiggle(network), run_time=t*0.1)
        self.play(FadeIn(cross, scale=0.5), network.animate.set_color(GRAY), run_time=t*0.05)
        
        brain_wipe = VGroup(
            MathTex(r"\circlearrowleft", color=RED_B, font_size=48),
            Text("Khởi tạo lại", font=F, font_size=32, color=RED_B),
            MathTex(r"\theta", color=RED_B, font_size=48)
        ).arrange(RIGHT, buff=0.15).move_to([0, 1.8, 0])
        
        self.play(FadeIn(brain_wipe, shift=UP), Rotate(cross, angle=PI/2), run_time=t*0.1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[1]
        title2 = Text("Meta-Learning: Học cách học", font=F, font_size=38, color=BLUE_B).to_edge(UP)

        omega_node = Circle(color=YELLOW_B, fill_opacity=0.3, radius=1.0).move_to([0, 1.5, 0])
        omega_txt = MathTex(r"\phi", font_size=60, color=YELLOW_B).move_to(omega_node)
        
        tasks = [Circle(color=GREEN_B, radius=0.5).move_to([x, -1.8, 0]) for x in [-4.5, -1.5, 1.5, 4.5]]
        task_lbls = [MathTex(f"T_{i+1}", font_size=36).move_to(tasks[i]) for i in range(3)]
        task_lbls.append(MathTex("T_{new}", font_size=36, color=RED_B).move_to(tasks[3]))
        
        self.play(Write(title2), run_time=t*0.1)
        self.play(GrowFromCenter(omega_node), Write(omega_txt), run_time=t*0.1)
        self.play(omega_node.animate.scale(1.1).set_color(ORANGE), rate_func=there_and_back, run_time=t*0.1)

        self.play(AnimationGroup(*[Create(t_obj) for t_obj in tasks[:3]], lag_ratio=0.1), run_time=t*0.15)
        self.play(AnimationGroup(*[Write(l) for l in task_lbls[:3]], lag_ratio=0.1), run_time=t*0.1)
        
        arrows = [Arrow(omega_node.get_bottom(), t_obj.get_top(), color=GRAY_C, buff=0.1, stroke_width=4) for t_obj in tasks[:3]]
        self.play(AnimationGroup(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=t*0.1)
        self.play(LaggedStart(*[Indicate(t_obj, color=YELLOW) for t_obj in tasks[:3]], lag_ratio=0.1), run_time=t*0.1)

        self.play(Create(tasks[3]), Write(task_lbls[3]), run_time=t*0.05)
        fast_arrow = Arrow(omega_node.get_bottom(), tasks[3].get_top(), color=YELLOW_B, stroke_width=8, buff=0.1)
        flash = MathTex(r"\star", color=YELLOW, font_size=80).move_to(fast_arrow.get_center() + RIGHT*0.4)
        
        self.play(GrowArrow(fast_arrow), run_time=t*0.1)
        self.play(FadeIn(flash, scale=2), tasks[3].animate.set_fill(YELLOW, opacity=0.5), run_time=t*0.1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[2]
        title3 = Text("MAML: Chọn điểm khởi tạo", font=F, font_size=38, color=BLUE_B).to_edge(UP)

        contours = VGroup(*[Ellipse(width=i*1.8, height=i*1.0, color=BLUE, stroke_opacity=0.6-i*0.08) for i in range(1, 8)])
        contours.shift(DOWN*0.5 + RIGHT*2)
        
        w1 = Dot([-4.5, 2.0, 0], color=RED_B, radius=0.15)
        lw1= MathTex(r"\theta_{random}", color=RED_B, font_size=32).next_to(w1, UP, 0.1)
        target = Dot(contours[0].get_center(), color=GREEN_B, radius=0.2)
        ltar   = MathTex(r"\theta^*", color=GREEN_B, font_size=36).next_to(target, DOWN, 0.1)

        path1 = TracedPath(w1.get_center, stroke_color=RED_A, stroke_width=4)
        
        w2  = Dot([-3.0, -1.0, 0], color=YELLOW_B, radius=0.15)
        lw2 = MathTex(r"\theta_0 \text{ (MAML)}", color=YELLOW_B, font_size=32).next_to(w2, DOWN, 0.1)
        path2 = Arrow(w2.get_center(), target.get_center(), color=YELLOW_B, buff=0.1, stroke_width=6)

        self.play(Write(title3), Create(contours, lag_ratio=0.1), run_time=t*0.15)
        self.play(FadeIn(target), Write(ltar), FadeIn(w1), Write(lw1), run_time=t*0.1)
        
        self.add(path1)
        self.play(w1.animate.move_to([-2, 2.5, 0]), run_time=t*0.1)
        self.play(w1.animate.move_to([0, 2.0, 0]), run_time=t*0.05)
        self.play(w1.animate.move_to(target.get_center() + UP*0.2), run_time=t*0.05)

        self.play(FadeIn(w2, scale=0.5), Write(lw2), run_time=t*0.1)
        self.play(GrowArrow(path2), run_time=t*0.1)
        self.play(Circumscribe(path2, color=YELLOW, time_width=0.5), run_time=t*0.1)

        hessian = MathTex(r"\nabla^2 \mathcal{L}", color=RED, font_size=120).move_to([-3, 0, 0])
        box_heavy = SurroundingRectangle(hessian, color=RED, fill_opacity=0.3, buff=0.3)
        
        self.play(FadeIn(hessian, shift=DOWN), Create(box_heavy), run_time=t*0.1)
        self.play(Wiggle(Group(hessian, box_heavy)), run_time=t*0.1)
        self.play(Group(hessian, box_heavy).animate.scale(1.5).set_opacity(0), run_time=t*0.05)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[3]
        title4 = Text("Mô hình quá nhiều tham số", font=F, font_size=38, color=RED_B).to_edge(UP)

        ax4 = Axes(x_range=[0, 250, 50], y_range=[0, 250, 50], x_length=8, y_length=5).shift(DOWN*0.5)
        self.play(Write(title4), Create(ax4), run_time=t*0.1)

        dots = VGroup()
        for i in range(25):
            val = max(5, 220 * np.exp(-i*0.5))
            dot = Dot(ax4.c2p(i*10, 250), color=YELLOW_B, radius=0.1) 
            dots.add(dot)
            self.play(dot.animate.move_to(ax4.c2p(i*10, val)), run_time=t*0.01)
        
        area = ax4.get_area(ax4.plot(lambda x: 220 * np.exp(-x/10), x_range=[0, 250]), color=BLUE, opacity=0.4)
        self.play(FadeIn(area), run_time=t*0.15)

        redundant_box = Rectangle(width=5.5, height=1.5, color=RED_A).move_to(ax4.c2p(160, 30))
        txt_thua = Text("Vùng dư thừa (≈ 0)", font=F, font_size=24, color=RED_A).next_to(redundant_box, UP)
        
        self.play(Create(redundant_box), FadeIn(txt_thua, shift=UP), run_time=t*0.15)
        self.play(Indicate(redundant_box, color=RED), run_time=t*0.1)
        
        subspace = Rectangle(width=2.5, height=5, color=GREEN_B, fill_opacity=0.5).move_to(ax4.c2p(15, 125))
        txt_sub = Text("Subspace\n(Quan trọng)", font=F, font_size=24, color=GREEN).move_to(subspace)
        self.play(Create(subspace), Write(txt_sub), run_time=t*0.25)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[4]
        title5 = Text("Vật lý: Số chiều nội tại rất nhỏ", font=F, font_size=38, color=GREEN_B).to_edge(UP)

        pivot  = Dot(UP*1.8, color=WHITE)
        string = Line(UP*1.8, ORIGIN, color=WHITE, stroke_width=3)
        bob    = Circle(radius=0.4, color=BLUE_D, fill_opacity=1).move_to(ORIGIN)
        pend   = VGroup(pivot, string, bob).move_to([-3.5, 0, 0])

        eq = MathTex(r"x(t) = A\cos(\omega t + \varphi)", font_size=48).move_to([2, 1.5, 0])
        
        box_244 = Rectangle(width=3.5, height=3.5, color=RED_B, fill_opacity=0.2).move_to([2, -1.5, 0])
        txt_244 = MathTex(r"\theta \in \mathbb{R}^{244}", font_size=40).move_to(box_244)
        
        box_8 = Rectangle(width=1.2, height=1.2, color=GREEN_B, fill_opacity=0.6).move_to([2, -1.5, 0])
        txt_8 = MathTex(r"z \in \mathbb{R}^{8}", font_size=28).move_to(box_8)

        scene5_grp = VGroup(pend, eq, box_244, txt_244, box_8, txt_8).scale(1.1)

        self.play(Write(title5), Create(pend), run_time=t*0.15)

        def pend_updater(mob, alpha):
            angle = 0.5 * np.sin(alpha * 4 * PI)
            p_center = np.array([-3.5, 1.0, 0])
            end = p_center + 3.0 * np.array([np.sin(angle), -np.cos(angle), 0])
            string.put_start_and_end_on(p_center, end)
            bob.move_to(end)

        self.play(UpdateFromAlphaFunc(pend, pend_updater), Write(eq), run_time=t*0.45)
        
        self.play(Create(box_244), Write(txt_244), run_time=t*0.15)
        self.play(Transform(box_244, box_8), Transform(txt_244, txt_8), run_time=t*0.25)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[5]
        title6 = Text("LEO: Giảm chiều nhưng vẫn lặp", font=F, font_size=38, color=ORANGE).to_edge(UP)

        maml_loop = Circle(radius=2.2, color=RED_B, stroke_width=6).move_to([-3.5, -0.5, 0])
        maml_arrow = Arrow(maml_loop.point_at_angle(PI/2), maml_loop.point_at_angle(PI/2-0.01), color=RED_B)
        m_txt = MathTex(r"\mathbb{R}^{244}", font_size=48).move_to(maml_loop)

        leo_loop = Circle(radius=1.0, color=YELLOW_B, stroke_width=6).move_to([3.5, -0.5, 0])
        leo_arrow = Arrow(leo_loop.point_at_angle(PI/2), leo_loop.point_at_angle(PI/2-0.01), color=YELLOW_B)
        l_txt = MathTex(r"\mathbb{R}^{20}", font_size=36).move_to(leo_loop)

        vs_arrow = Arrow(maml_loop.get_right(), leo_loop.get_left(), color=WHITE, stroke_width=8)

        self.play(Write(title6), run_time=t*0.15)
        self.play(Create(maml_loop), Create(maml_arrow), Write(m_txt), run_time=t*0.2)
        self.play(GrowArrow(vs_arrow), run_time=t*0.1)
        self.play(Create(leo_loop), Create(leo_arrow), Write(l_txt), run_time=t*0.2)
        
        self.play(Rotate(maml_loop, angle=-2*PI, run_time=t*0.35), Rotate(leo_loop, angle=-6*PI, run_time=t*0.35))
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[6]
        title7 = Text("Manifold Meta-Learning: Xóa bỏ Inner Loop", font=F, font_size=38, color=GREEN_C).to_edge(UP)

        outer_loop = Circle(radius=2.5, color=BLUE_B, stroke_width=6).move_to([-3.5, 0, 0])
        inner_loop = Circle(radius=1.0, color=RED_B, stroke_width=6).move_to([-3.5, 0, 0])
        txt_outer = Text("Outer Loop", font=F, font_size=24).next_to(outer_loop, UP)
        txt_inner = Text("Inner Loop", font=F, font_size=20, color=RED_B).move_to(inner_loop)

        self.play(Write(title7), run_time=t*0.1)
        self.play(Create(outer_loop), Write(txt_outer), run_time=t*0.1)
        self.play(Create(inner_loop), Write(txt_inner), run_time=t*0.1)
        
        self.play(Rotate(inner_loop, angle=-4*PI, run_time=t*0.15))

        cross = MathTex(r"\times", color=RED, font_size=150).move_to(inner_loop)
        self.play(FadeIn(cross, scale=0.5), run_time=t*0.1)
        self.play(FadeOut(inner_loop), FadeOut(txt_inner), FadeOut(cross), run_time=t*0.05)

        data_node = Text("Dataset", font=F, font_size=32).move_to([-0.5, 0, 0])
        enc_box = Rectangle(width=2.5, height=1.8, color=GREEN_C, fill_opacity=0.4).move_to([4.0, 0, 0])
        enc_txt = Text("Encoder E_ψ\n(1 Forward Pass)", font=F, font_size=20, color=WHITE).move_to(enc_box)
        
        arr_to_enc = Arrow(data_node.get_right(), enc_box.get_left(), color=WHITE, buff=0.2, stroke_width=6)
        
        self.play(FadeIn(data_node, shift=RIGHT), run_time=t*0.1)
        self.play(GrowArrow(arr_to_enc), run_time=t*0.05)
        self.play(Create(enc_box), Write(enc_txt), run_time=t*0.1)

        phi_out = MathTex(r"\phi", font_size=60, color=YELLOW).next_to(enc_box, DOWN, 0.5)
        arr_to_phi = Arrow(enc_box.get_bottom(), phi_out.get_top(), color=YELLOW, stroke_width=6)
        
        self.play(GrowArrow(arr_to_phi), FadeIn(phi_out, shift=DOWN), run_time=t*0.1)
        self.play(Circumscribe(enc_box, color=GREEN, time_width=0.5), run_time=t*0.05)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[7]
        title8 = Text("Lifting: Chuyển đổi số chiều", font=F, font_size=38, color=BLUE_C).to_edge(UP)

        phi_vec = VGroup(*[Square(side_length=0.4, color=GREEN_B, fill_opacity=0.6) for _ in range(4)]).arrange(DOWN, buff=0.05).move_to([-4.5, 0.5, 0])
        phi_lbl = MathTex(r"\hat{\phi} \in \mathbb{R}^{20}", font_size=36, color=GREEN_B).next_to(phi_vec, DOWN, buff=0.3)

        mat_V = Rectangle(width=2.5, height=3.5, color=BLUE_C, fill_opacity=0.3).move_to([0, 0.5, 0])
        mat_lbl = MathTex(r"\times V", font_size=60, color=BLUE_C).move_to(mat_V)
        
        theta_vec = VGroup(*[Square(side_length=0.2, color=RED_B, fill_opacity=0.6) for _ in range(16)]).arrange(DOWN, buff=0.03).move_to([4.5, 0.5, 0])
        theta_lbl = MathTex(r"\theta \in \mathbb{R}^{244}", font_size=36, color=RED_B).next_to(theta_vec, DOWN, buff=0.3)

        self.play(Write(title8), run_time=t*0.1)
        self.play(FadeIn(phi_vec, shift=DOWN), Write(phi_lbl), run_time=t*0.15)
        self.play(Create(mat_V), Write(mat_lbl), run_time=t*0.15)

        phi_copy = phi_vec.copy()
        self.play(phi_copy.animate.move_to(mat_V.get_left() + LEFT*0.3), run_time=t*0.15)
        self.play(Transform(phi_copy, theta_vec), run_time=t*0.2)
        self.play(Write(theta_lbl), run_time=t*0.1)

        eq_lift = MathTex(r"\theta = V\phi + \theta_{bias}", font_size=48, color=YELLOW).move_to([0, -3.0, 0])
        self.play(Write(eq_lift), run_time=t*0.05)
        self.play(Indicate(eq_lift), run_time=t*0.1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[8]
        title9 = Text("Huấn luyện: ", font=F, font_size=38, color=BLUE_C).to_edge(UP)

        box_E = Rectangle(width=2.5, height=1.5, color=GREEN).move_to([-4, 0, 0])
        txt_e = Text("Encoder", font=F, font_size=28).move_to(box_E)
        
        box_L = Rectangle(width=2.5, height=1.5, color=BLUE).move_to([0, 0, 0])
        txt_l = Text("Lifting", font=F, font_size=28).move_to(box_L)
        
        box_F = Rectangle(width=2.5, height=1.5, color=ORANGE).move_to([4, 0, 0])
        txt_f = Text("Model F", font=F, font_size=28).move_to(box_F)
        
        fw_arr1 = Arrow(box_E.get_right(), box_L.get_left(), buff=0.2, color=WHITE, stroke_width=6)
        fw_arr2 = Arrow(box_L.get_right(), box_F.get_left(), buff=0.2, color=WHITE, stroke_width=6)
        
        bw_arr = Arrow(box_F.get_bottom() + DOWN*0.6, box_E.get_bottom() + DOWN*0.6, color=YELLOW, buff=0, stroke_width=6)
        bw_txt = Text("Backprop (First-Order)", font=F, font_size=24, color=YELLOW).next_to(bw_arr, DOWN)

        scene9_content = VGroup(box_E, txt_e, box_L, txt_l, box_F, txt_f, fw_arr1, fw_arr2, bw_arr, bw_txt)
        scene9_content.scale(1.2).shift(DOWN*0.5) 

        self.play(Write(title9), run_time=t*0.15)
        self.play(Create(box_E), Write(txt_e), Create(box_L), Write(txt_l), Create(box_F), Write(txt_f), run_time=t*0.25)
        
        self.play(GrowArrow(fw_arr1), GrowArrow(fw_arr2), run_time=t*0.2)
        self.play(GrowArrow(bw_arr), Write(bw_txt), run_time=t*0.2)
        
        self.play(ShowPassingFlash(bw_arr.copy().set_color(RED), time_width=0.5), run_time=t*0.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[9]
        title10 = Text("Bouc-Wen: Nhận dạng hệ thống & Phân phối", font=F, font_size=38, color=TEAL_B).to_edge(UP)

        # Trục tọa độ cho tín hiệu Input u_i
        ax_in = Axes(x_range=[0, 10, 2], y_range=[-1, 1, 1], x_length=2.5, y_length=1.5).move_to([-4, 1.5, 0])
        graph_in = ax_in.plot(lambda x: np.sin(x), color=YELLOW)
        lbl_in = MathTex(r"u_i(t)", font_size=28).next_to(ax_in, UP, 0.1)

        # Hộp hệ thống S_i (Bouc-Wen)
        sys_box = Rectangle(width=2.8, height=2.2, color=BLUE_C, fill_opacity=0.2).move_to([0, 1.5, 0])
        sys_txt = Text("Hệ thống S_i\n(Bouc-Wen)", font=F, font_size=24).move_to(sys_box)
        z_txt = MathTex(r"z_i \in \mathbb{R}^8", font_size=28, color=YELLOW).next_to(sys_txt, DOWN, 0.2)

        # Trục tọa độ cho tín hiệu Output y_i (Hysteresis loop)
        ax_out = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=2, y_length=2).move_to([4, 1.5, 0])
        graph_out = ax_out.plot_parametric_curve(
            lambda x: np.array([np.sin(x), np.sin(x) - 0.5*np.cos(x), 0]), 
            t_range=[0, 2*PI], color=RED
        )
        lbl_out = MathTex(r"y_i(t)", font_size=28).next_to(ax_out, UP, 0.1)

        arr1 = Arrow(ax_in.get_right(), sys_box.get_left(), color=WHITE, buff=0.1)
        arr2 = Arrow(sys_box.get_right(), ax_out.get_left(), color=WHITE, buff=0.1)

        # Đa tạp phân phối bên dưới
        mani_ax = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=6, y_length=2.5).move_to([0, -1.8, 0])
        mani_curve = mani_ax.plot(lambda x: 0.3*x**2 - 1, color=GRAY, stroke_width=4)
        mani_lbl = VGroup(
            Text("Phân phối", font=F, font_size=24, color=GRAY),
            MathTex(r"p(D)", font_size=28, color=GRAY),
            Text("đa dạng", font=F, font_size=24, color=GRAY)
        ).arrange(RIGHT, buff=0.15).next_to(mani_curve, DOWN, 0.1)
        
        dots = VGroup(*[Dot(mani_ax.c2p(x, 0.3*x**2 - 1), color=GREEN, radius=0.08) for x in np.linspace(-2.5, 2.5, 12)])
        out_of_dist_dot = Dot(mani_ax.c2p(-2, 1.5), color=RED, radius=0.1)
        ood_txt = Text("Ngoài phân phối", font=F, font_size=18, color=RED).next_to(out_of_dist_dot, RIGHT)

        # Khớp hoạt ảnh với audio
        self.play(Write(title10), run_time=t*0.1)
        self.play(Create(ax_in), Create(graph_in), Write(lbl_in), run_time=t*0.15) # "input là tín hiệu lực kích thích..."
        self.play(GrowArrow(arr1), Create(sys_box), Write(sys_txt), run_time=t*0.15) # "Bouc-Wen là mô hình..."
        self.play(GrowArrow(arr2), Create(ax_out), Create(graph_out), Write(lbl_out), run_time=t*0.15) # "output là chuyển vị..."
        self.play(Write(z_txt), run_time=t*0.1) # "8 tham số vật lý ẩn z_i..."
        self.play(Create(mani_ax), Create(mani_curve), Write(mani_lbl), run_time=t*0.1)
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=t*0.1) # "Tạo nên sự đa dạng trong phân phối..."
        self.play(FadeIn(out_of_dist_dot), Write(ood_txt), run_time=t*0.05) # "Nếu quá đa dạng và nằm ngoài..."
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[10]
        title11 = Text("Kiến trúc F: Neural State-Space Model", font=F, font_size=38, color=ORANGE).to_edge(UP)

        # Mô tả 3 trạng thái vật lý
        state_box = Rectangle(width=4.5, height=2.5, color=GRAY_B, fill_opacity=0.1).move_to([-3.5, 0.5, 0])
        state_title = Text("3 Trạng thái Ẩn", font=F, font_size=26, color=YELLOW).next_to(state_box, UP, 0.1)
        
        s1 = VGroup(MathTex(r"x:", font_size=32), Text("vị trí", font=F, font_size=24)).arrange(RIGHT, buff=0.2)
        s2 = VGroup(MathTex(r"v:", font_size=32), Text("vận tốc", font=F, font_size=24)).arrange(RIGHT, buff=0.2)
        s3 = VGroup(MathTex(r"z:", font_size=32), Text("lực hysteresis", font=F, font_size=24)).arrange(RIGHT, buff=0.2)
        
        # Gộp và căn lề trái cho 3 dòng trạng thái
        VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.5, 0.5, 0])

        # Mô tả công thức Toán học state-space
        eq_box = Rectangle(width=5.5, height=2.5, color=BLUE_E, fill_opacity=0.1).move_to([3, 0.5, 0])
        eq_title = Text("Cập nhật trạng thái", font=F, font_size=26, color=BLUE_B).next_to(eq_box, UP, 0.1)
        
        eq_lin = VGroup(
            MathTex(r"x_{k+1} = A x_k + B u_k", font_size=32),
            Text("— Tuyến tính (Ổn định)", font=F, font_size=18, color=GREEN_B)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3, 1.2, 0])

        eq_non = VGroup(
            MathTex(r"+ \mathcal{N}_f(x_k, u_k)", font_size=32),
            Text("— Phi tuyến (Mạng NN)", font=F, font_size=18, color=YELLOW_B)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3, -0.1, 0])

        param_txt = VGroup(
            Text("Tham số:", font=F, font_size=28, color=RED_B),
            MathTex(r"\theta \in \mathbb{R}^{244} \gg 8", font_size=36, color=RED_B),
            Text("(biến vật lý)", font=F, font_size=28, color=RED_B)
        ).arrange(RIGHT, buff=0.15).move_to([0, -2.5, 0])
        
        glow_param = param_txt.copy().set_color(YELLOW).set_stroke(width=3)

        self.play(Write(title11), run_time=t*0.1)

        self.play(Create(state_box), Write(state_title), run_time=t*0.1)
        self.play(Write(s1), run_time=t*0.1)
        self.play(Write(s2), run_time=t*0.1)
        self.play(Write(s3), run_time=t*0.1)

        self.play(Create(eq_box), Write(eq_title), run_time=t*0.1)
        self.play(Write(eq_lin), run_time=t*0.15)
        self.play(Write(eq_non), run_time=t*0.15)

        self.play(FadeIn(param_txt, shift=UP), run_time=t*0.05)
        self.play(ShowPassingFlash(glow_param, time_width=0.5), run_time=t*0.05)
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[11]
        title12 = Text("Kết Quả: Cân bằng Dữ liệu và Tham số", font=F, font_size=38, color=BLUE_B).to_edge(UP)

        ax = Axes(x_range=[100, 5000, 1000], y_range=[0, 100, 20], x_length=9, y_length=5.5).shift(DOWN*0.2)
        curve_full = ax.plot(lambda x: min(99, 100*(1-np.exp(-x/1200))), color=RED_B, stroke_width=5)
        curve_20   = ax.plot(lambda x: min(97.5, 65 + 32.5*np.tanh(x/600)), color=GREEN_B, stroke_width=5)
        
        leg = VGroup(
            MathTex(r"\text{Full-order (244D)}", color=RED_B, font_size=36),
            MathTex(r"\text{Manifold (20D)}", color=GREEN_B, font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ax.c2p(3500, 30))

        star = MathTex(r"\star", font_size=60, color=YELLOW).move_to(ax.c2p(500, 95.2))
        vline = ax.get_vertical_line(ax.c2p(500, 95.2), color=YELLOW, line_func=DashedLine)
        
        self.play(Write(title12), Create(ax), run_time=t*0.2)
        self.play(Create(curve_full), Create(curve_20), FadeIn(leg), run_time=t*0.4)
        self.play(Create(vline), FadeIn(star, scale=2), run_time=t*0.25)
        self.play(Indicate(star, color=YELLOW, scale_factor=1.5), run_time=t*0.15)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[12]
        title13 = Text("Hybrid: Khởi tạo thông minh + AdamW", font=F, font_size=38, color=TEAL_B).to_edge(UP)

        contours = VGroup(*[Ellipse(width=i*1.8, height=i*1.0, color=BLUE, stroke_opacity=0.8-i*0.1) for i in range(1, 7)])
        contours.shift(DOWN*0.5 + RIGHT*2)
        
        center = Dot(contours[0].get_center(), color=YELLOW, radius=0.15)
        math_phi = MathTex(r"\phi^*", font_size=40).next_to(center, DOWN)

        dot_rand = Dot([-4, 2.5, 0], color=RED, radius=0.12)
        path_rand = Arrow(dot_rand.get_center(), center.get_center(), color=RED, path_arc=0.5, stroke_width=4)
        txt_rand = Text("Ngẫu nhiên", font=F, font_size=24, color=RED).next_to(dot_rand, UP)

        dot_enc = Dot([1, -0.5, 0], color=GREEN, radius=0.15)
        path_enc_jump = Arrow([-4, -2.5, 0], dot_enc.get_center(), color=GREEN, stroke_width=8)
        path_enc_walk = Arrow(dot_enc.get_center(), center.get_center(), color=YELLOW, buff=0.1, stroke_width=4)
        txt_enc = Text("Encoder", font=F, font_size=24, color=GREEN).next_to([-4, -2.5, 0], DOWN)

        self.play(Write(title13), Create(contours), Create(center), Write(math_phi), run_time=t*0.2)
        self.play(FadeIn(dot_rand), Write(txt_rand), run_time=t*0.15)
        self.play(GrowArrow(path_rand), run_time=t*0.2)
        
        self.play(GrowArrow(path_enc_jump), FadeIn(dot_enc), Write(txt_enc), run_time=t*0.2)
        self.play(GrowArrow(path_enc_walk), run_time=t*0.25)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        t = dur[13]
        title14 = Text("Hành trình tối ưu chi phí", font=F, font_size=38, color=BLUE_C).to_edge(UP)

        box_maml = Rectangle(width=3.0, height=1.8, color=RED_B).move_to([-4.5, 0.5, 0])
        txt_maml = Text("MAML\nO(n²)", font=F, font_size=28).move_to(box_maml)
        
        box_leo = Rectangle(width=3.0, height=1.8, color=ORANGE).move_to([0, 0.5, 0])
        txt_leo = Text("LEO\nO(z²)", font=F, font_size=28).move_to(box_leo)
        
        box_mani = Rectangle(width=3.0, height=1.8, color=GREEN_B).move_to([4.5, 0.5, 0])
        txt_mani = Text("Manifold\nO(1) Inference", font=F, font_size=28).move_to(box_mani)

        arr1 = Arrow(box_maml.get_right(), box_leo.get_left(), color=WHITE, stroke_width=6)
        arr2 = Arrow(box_leo.get_right(), box_mani.get_left(), color=WHITE, stroke_width=6)

        self.play(Write(title14), run_time=t*0.1)
        self.play(Create(box_maml), Write(txt_maml), run_time=t*0.1)
        self.play(GrowArrow(arr1), run_time=t*0.1)
        self.play(Create(box_leo), Write(txt_leo), run_time=t*0.1)
        self.play(GrowArrow(arr2), run_time=t*0.1)
        self.play(Create(box_mani), Write(txt_mani), run_time=t*0.15)
        
        glow = box_mani.copy().set_color(YELLOW).set_stroke(width=8)
        self.play(FadeIn(glow), rate_func=there_and_back, run_time=t*0.1)

        future_txt = Text("Tương lai: Variational Meta-Learning (Uncertainty)", font=F, font_size=28, color=TEAL_A).move_to([0, -1.8, 0])
        self.play(Write(future_txt), run_time=t*0.15)

        thanks = Text("Cảm ơn các bạn đã theo dõi!", font=F, font_size=36, color=YELLOW_B).to_edge(DOWN)
        
        self.play(Write(thanks), run_time=t*0.05) # Reduced from t*0.1 to t*0.05

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)