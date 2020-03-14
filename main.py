import argparse

from solutions import GA, SA, LocalSearch, VariableLocalSearch
from utils import data_reader, generate_gif, plot
from utils import euclidean_dist
from TSP import TSP

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str)
parser.add_argument('--thresh', type=float)
parser.add_argument('--savepath', type=str, default=None)
parser.add_argument('--save_freq', type=int, default=1000)
parser.add_argument('--print_freq', type=int, default=1000)
parser.add_argument('--max_itr', type=int, default=500000)
args = parser.parse_args()


def main():
    print('Starting...')
    data = data_reader(args.target)
    # solution = LocalSearch(op_idx=2)
    # solution = VariableLocalSearch(op_idx1=0, op_idx2=2, keep_invariant=1000, keep_invariant_max=2000)
    # solution = SA(op_idx=0, init_coeff=0.9, init_inner_time=200, stop_temp=1e-2, alpha=0.98)
    solution = GA(population_size=200, cross_rate=[0.3, 0.5], mutation_rate=[0.1, 0.5], keep_invariant=50)
    tsp = TSP(solution, data, euclidean_dist)
    tsp.run(threshhold=args.thresh, savepath=args.savepath, save_freq=args.save_freq,
            print_freq=args.print_freq, max_iteration=args.max_itr)
    if args.savepath is not None:
        generate_gif(args.savepath)
        plot(args.savepath)


if __name__ == '__main__':
    main()
