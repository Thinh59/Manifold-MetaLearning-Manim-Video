"""
Cách chạy: python src_video/generate_audio_1.py
"""
import asyncio
import edge_tts
import os


scripts = {
    "s01_intro": """
        Như chúng ta đã biết trong Machine Learning, bài toán supervised learning được đặt ra như sau:
        cho input x và nhãn y, ta tìm mô hình f-theta tối thiểu hóa hàm mất mát.
        Còn Deep learning tuy rằng rất mạnh, nhưng nó lại học từ đầu cho mỗi tác vụ,
        tối ưu toàn bộ theta thuộc R-n-theta từ khởi tạo ngẫu nhiên.
        Hệ quả: cần rất nhiều dữ liệu và không tái sử dụng được kinh nghiệm từ tác vụ trước.
        Ví dụ như mô hình đã học để phân biệt chó-mèo, khi gặp chim, nó lại phải học lại từ đầu hoặc là cho ra kết quả dự đoán sai là chó hoặc mèo nếu không được học lại.
    """,

    "s02_meta_learning": """
        Vì vậy, chúng ta có một khái niệm mới là Meta-learning - phương pháp này xem xét bài toán hoàn toàn khác.
        Thay vì tối ưu theta cho từng tác vụ đơn lẻ,
        ta tối ưu phi — tham số học cách học — trên toàn bộ phân phối tác vụ p(T).
        Vòng lặp ngoài học phi trên nhiều tác vụ nguồn.
        Vòng lặp trong thích nghi theta cho từng tác vụ cụ thể.
        Từ đó đạt được mục tiêu: khi gặp tác vụ mới, mô hình chỉ cần vài bước gradient là có thể đạt kết quả tốt.
    """,

    "s03_maml": """
        Trong đó phải kể đến là MAML. Một phương pháp chọn phi chính là điểm khởi tạo theta-không tối ưu.
        Lý luận: nếu tồn tại theta-không sao cho gradient descent chỉ cần vài bước
        là đạt đến theta tốt với bất kỳ tác vụ nào thì ta đã học được cấu trúc chung.
        Tuy nhiên, để tối ưu theta-không, phải tính gradient qua cả vòng lặp trong —
        tức là đạo hàm của đạo hàm, bậc hai.
        Với 244 tham số, ma trận Hessian rất lớn — đây là nút thắt về tính toán.
    """,

    "s04_blackbox_limits": """
        Vấn đề cốt lõi là một nghịch lý: mô hình càng nhiều tham số thì càng biểu đạt tốt —
        nhưng chi phí second-order optimization tăng bậc hai với số tham số.
        Bằng chứng là từ việc phân tích trị riêng của Hessian tại nghiệm 
        cho thấy đa số trị riêng xấp xỉ không, điều này cho thấy mô hình dư thừa tham số.
        Kết luận quan trọng: không gian R-244 là dư thừa. 
        Nghĩa là, chỉ cần một không gian con với chiều nhỏ hơn là đủ để mô tả toàn bộ lớp hệ thống.
    """,

    "s05_physics": """
        Hãy nhìn vào mô hình vật lý để thấy điều này trực quan hơn.
        Con lắc đơn có vô số trạng thái — nhưng toàn bộ chuyển động
        được xác định hoàn toàn bởi ba tham số: biên độ A, tần số góc omega, và pha phi.
        Đây là hệ có số chiều quyết định thấp dù không gian quan sát có chiều cao hơn.
        Tương tự, lớp hệ thống Bouc-Wen cũng chỉ có 8 tham số vật lý biến đổi —
        trong khi mô hình neural có tới 244 tham số.
        Vì vậy, nếu ta học được không gian con có số chiều thấp (xấp xỉ 20) nhưng có thể biểu diễn được toàn bộ sự biến đổi thực sự,
        thì 224 chiều còn lại là dư thừa.
    """,

    "s06_leo": """
        LEO — Latent Embedding Optimization — đã dựa trên hướng đi này:
        thay vì tối ưu theta trong R-244, chúng tối ưu z trong R-20 rồi giải mã.
        Từ đó, cho ra bề mặt loss phẳng hơn, gradient rõ ràng hơn.
        Nhưng LEO vẫn giữ vòng lặp bên trong: với mỗi tác vụ, vẫn chạy gradient descent để tìm z tối ưu.
        Điều này vẫn đòi hỏi tính đạo hàm bậc hai qua vòng lặp trong.
        Như vậy, LEO giảm chiều không gian, nhưng không giảm số vòng lặp.
        Đây là điểm yếu còn lại cần giải quyết.
    """,

    "s07_manifold_idea": """
        Từ ý tưởng LEO, chúng ta có Manifold Meta-Learning. Phương pháp này đặt ra một câu hỏi then chốt:
        có nhất thiết phải dùng gradient descent để tìm tham số phi mũ cho mỗi tác vụ không?
        Câu trả lời là không — nếu ta học được một hàm trực tiếp rút từ dữ liệu ra tham số phi mũ.
        Ý tưởng cốt lõi: thay vòng lặp bên trong bằng một mạng Encoder E-psi,
        một giải thuật học sẵn cách đọc dataset
        và xuất ra phi chỉ trong một lần forward pass duy nhất.
        Chi phí tính toán giảm từ nhiều bước gradient xuống còn một lần forward pass.
    """,

    "s08_lifting": """
        Từ phi mũ 20 chiều, hàm Lifting tuyến tính chuyển về theta 244 chiều:
        theta bằng V nhân phi, sau đó cộng theta-bias.
        Tại sao lại dùng hàm tuyến tính? Vì manifold là affine subspace —
        nên hàm tuyến tính là đủ biểu đạt cho lớp hệ thống Bouc-Wen,
        đồng thời gradient qua Lifting là hằng số, giúp tối ưu ổn định hơn.
        Toàn bộ kiến trúc là encoder-decoder:
        encoder đọc dữ liệu train xuất phi,
        decoder gồm Lifting rồi F xuất dự đoán trên dữ liệu test.
    """,

    "s09_loss": """
        Toàn bộ hệ thống được huấn luyện end-to-end qua hàm loss J Monte Carlo.
        Điểm quan trọng: ta tối ưu đồng thời gamma — tham số Lifting — và psi — tham số Encoder.
        Gradient chỉ cần first-order, không cần Hessian —
        đây là lợi thế trực tiếp từ việc loại bỏ inner loop.
        Mỗi batch 128 dataset, mỗi dataset tính loss trên phần test,
        rồi backprop qua toàn bộ đồ thị một lần.
        200 nghìn iteration với Adam, mất khoảng 25 tiếng.
    """,

    "s10_distribution": """
        Tiếp đến, hãy tìm hiểu bài toán chúng ta đang giải.
        Bouc-Wen là mô hình hysteresis nổi tiếng trong kỹ thuật cấu trúc — dùng để mô tả ứng xử phi tuyến
        của vật liệu và thiết bị giảm chấn dưới tải động, như cách tòa nhà hấp thụ năng lượng động đất.
        Đây là bài toán system identification có giám sát — supervised learning:
        input là tín hiệu lực kích thích hoặc chuyển vị u_i theo thời gian,
        output là chuyển vị hoặc lực phản hồi y_i tương ứng — đo được từ cảm biến thực tế.
        Mục tiêu là học hàm ánh xạ từ chuỗi input sang chuỗi output, thích nghi nhanh khi gặp hệ mới.
        Mỗi dataset D_i được sinh bởi một hệ thống S_i với 8 tham số vật lý ẩn z_i khác nhau —
        chính 8 tham số này tạo nên sự đa dạng trong phân phối p(D) mà Manifold phải học.
        Điều kiện đủ để bài toán có nghiệm: chiều phi phải lớn hơn hoặc bằng chiều z.
        Nếu meta-dataset không đủ đa dạng, manifold học được sẽ suy biến.
        Nếu quá đa dạng và nằm ngoài phân phối, mô hình không học được cấu trúc chung.
        Đây là yêu cầu về phân phối dữ liệu, không phải chỉ là về lượng dữ liệu.
    """,

    "s11_model_f": """
        Để giải bài toán này, mô hình cơ sở F được thiết kế là Neural State-Space Model.
        Với mỗi bước thời gian, mô hình nhận vào tín hiệu điều khiển u — chẳng hạn lực kích thích —
        và xuất ra tín hiệu quan sát y — chẳng hạn chuyển vị hoặc lực phản hồi đo được.
        Bên trong là 3 trạng thái ẩn phản ánh đúng 3 biến vật lý của Bouc-Wen:
        vị trí, vận tốc, và lực hysteresis — không phải trạng thái tùy ý.
        Trạng thái tiếp theo bằng tổng phần tuyến tính A-x cộng B-u
        và phần nonlinear N-f học phần dư hysteresis còn lại.
        Tại sao lại thiết kế như vậy? Vì phần tuyến tính đảm bảo gradient flow tốt và ổn định số học,
        còn phần nonlinear N-f và N-g mô hình hóa đặc trưng phi tuyến đặc thù của Bouc-Wen.
        244 tham số — over-parameterized so với 8 biến ẩn vật lý — chính là động lực
        để học một manifold 20 chiều thay vì tối ưu trực tiếp trong không gian đầy đủ.
    """,

    "s12_results": """
        Kết quả thực nghiệm xác nhận được lý luận trên.
        Với chỉ 500 mẫu: bài toán reduced-order 20 chiều đạt median FIT 95.2 phần trăm,
        trong khi full-order với cùng dữ liệu đó vẫn dưới baseline tuyến tính 77.2 phần trăm.
        Lý do: cấu trúc manifold 20 chiều đã mã hóa prior knowledge về lớp hệ thống —
        quá trình tối ưu chỉ cần tìm 20 số thay vì 244.
        Trên 2000 mẫu, full-order bắt đầu vượt vì dữ liệu đủ để khai thác toàn bộ sức chứa.
        Đây là trade-off rõ ràng: ít dữ liệu ưu tiên manifold, nhiều dữ liệu lại ưu tiên full-order.
    """,

    "s13_hybrid": """
        Tuy Encoder E-psi cho kết quả tốt nhưng chưa tối ưu —
        vì nó chỉ là xấp xỉ của việc tối ưu, không phải tối ưu thực sự.
        Giải pháp là kết hợp giữa dùng E-psi như warm start thông minh —
        cho ra phi-không gần vùng tối ưu —
        rồi chạy AdamW trên bài toán reduced-complexity để tinh chỉnh.
        Cụ thể, AdamW từ phi-không tốt hội tụ trong 10 nghìn bước
        thay vì 50 nghìn từ khởi tạo ngẫu nhiên.
        Toàn bộ vẫn trong không gian 20 chiều nên ít tốn kém hơn full-order.
    """,

    "s14_conclusion": """
        Nhìn lại hành trình từ MAML đến Manifold, ta thấy đó là hành trình giảm thiểu chi phí tính toán
        mà không làm giảm khả năng biểu đạt.
        Trong khi, MAML: tối ưu trong R-n-theta với second-order gradient.
        và LEO: giảm xuống R-n-z nhưng vẫn inner loop.
        Thì Manifold: loại bỏ hoàn toàn inner loop, thay bằng một forward pass —
        amortize chi phí vào meta-training thay vì inference.
        Mỗi bước đều có lý luận toán học rõ ràng, không chỉ là thực nghiệm.
        Trong tương lai, variational meta-learning trên manifold
        sẽ cho phép uncertainty quantification — một bước tiếp theo tự nhiên.
        Cảm ơn các bạn đã theo dõi!
    """
}


async def generate_all():
    os.makedirs("audio", exist_ok=True)
    for name, text in scripts.items():
        clean_text = " ".join(text.split())
        filename = f"audio/{name}.mp3"
        max_retries = 3
        success = False

        for attempt in range(max_retries):
            try:
                communicate = edge_tts.Communicate(
                    clean_text,
                    voice="vi-VN-NamMinhNeural",
                    rate = "+15%"
                )
                await communicate.save(filename)
                print(f"Success: {filename}")
                success = True
                break
            except Exception as e:
                print(f"  Attempt {attempt+1} failed ({name}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 * (attempt + 1))

        if not success:
            try:
                print(f"  Falling back to gTTS for {name}...")
                from gtts import gTTS
                tts = gTTS(text=clean_text, lang="vi")
                tts.save(filename)
                print(f"Success gTTS: {filename}")
            except Exception as e2:
                print(f"Error generating {name}: {e2}")

        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(generate_all())