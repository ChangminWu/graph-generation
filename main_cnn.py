from train_cnn import *


class Args():
    def __init__(self):
        self.batch_size = 1
        self.epochs = 800
        self.epochs_log = 1
        self.seed = 1
        self.shuffle = True
        self.shuffle_neighbour = False
        self.num_workers = 2
        self.lr = 0.001
        self.momentum = 0.5

        self.input_size = 16
        self.hops = 3
        self.max_degree = 9

        # for karate_club dataset
        self.start_idx = 30
        self.end_idx = 35
        # for self generated dataset
        self.start_idx = 90
        self.end_idx = 100
if __name__ == '__main__':
    # clean logging directory
    if os.path.isdir("logs"):
        shutil.rmtree("logs")
    configure("logs/logs_toy", flush_secs=30)

    args = Args()
    torch.manual_seed(args.seed)

    # G = nx.karate_club_graph()
    # G = nx.LCF_graph(14,[5,-5],7)
    # G = nx.LCF_graph(20,[-9,-9],10)
    G, embedding = Graph_synthetic(10)
    dataset = GraphDataset(G, shuffle_neighbour=args.shuffle_neighbour, hops=args.hops, max_degree=args.max_degree, embedding=embedding)

    embedding_size = dataset.embedding.size(1)
    encoder = Encoder(feature_size=embedding_size, input_size=args.input_size, layer_num=3).cuda(CUDA)
    decoder = CNN_decoder_share(encoder.input_size * 16, embedding_size, stride=3).cuda(CUDA)


    train(args,dataset, encoder, decoder)